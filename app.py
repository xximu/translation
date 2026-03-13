"""
AI翻译助手 - Flask应用
提供中文翻译成英文并提取关键词的功能
"""

from flask import Flask, render_template, request, jsonify
import requests
import config
import logging
import re
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 限流配置
RATE_LIMIT_CONFIG = {
    'max_requests_per_minute': 30,
    'max_requests_per_hour': 100
}

# 存储请求记录的字典
request_records = defaultdict(list)


def rate_limit(f):
    """
    限流装饰器，防止API滥用

    Returns:
        function: 包装后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取客户端IP
        client_ip = request.remote_addr
        now = datetime.now()

        # 清理过期的请求记录
        request_records[client_ip] = [
            timestamp for timestamp in request_records[client_ip]
            if now - timestamp < timedelta(hours=1)
        ]

        # 检查每分钟限流
        minute_ago_requests = [
            timestamp for timestamp in request_records[client_ip]
            if now - timestamp < timedelta(minutes=1)
        ]
        if len(minute_ago_requests) >= RATE_LIMIT_CONFIG['max_requests_per_minute']:
            logger.warning(f"IP {client_ip} 触发每分钟限流")
            return jsonify({
                "error": "请求过于频繁，请稍后再试"
            }), 429

        # 检查每小时限流
        if len(request_records[client_ip]) >= RATE_LIMIT_CONFIG['max_requests_per_hour']:
            logger.warning(f"IP {client_ip} 触发每小时限流")
            return jsonify({
                "error": "请求次数超过限制，请1小时后再试"
            }), 429

        # 记录本次请求
        request_records[client_ip].append(now)

        return f(*args, **kwargs)
    return decorated_function


def validate_and_sanitize_input(text):
    """
    验证和清理输入文本

    Args:
        text (str): 输入文本

    Returns:
        tuple: (is_valid: bool, error_message: str or None, sanitized_text: str)
    """
    if not text:
        return False, "输入内容不能为空", ""

    # 去除首尾空格
    text = text.strip()

    # 检查长度
    if len(text) > 1000:
        return False, "输入内容过长，请限制在1000字以内", ""

    # 检查是否包含潜在危险的字符序列
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',  # 脚本标签
        r'on\w+\s*=',  # 事件处理器
        r'javascript:',  # JavaScript协议
        r'<iframe',  # iframe标签
        r'<object',  # object标签
        r'<embed',  # embed标签
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"检测到潜在危险内容，模式: {pattern}")
            return False, "输入内容包含不安全的字符", ""

    # 检查是否包含中文
    if not re.search(r'[\u4e00-\u9fff]', text):
        return False, "请输入中文内容", ""

    return True, None, text


def parse_translation_result(content):
    """
    解析翻译API返回的内容

    Args:
        content (str): API返回的内容

    Returns:
        tuple: (translation: str, keywords: list)
    """
    translation = ""
    keywords = []

    # 尝试多种格式解析
    lines = content.strip().split('\n')

    for line in lines:
        line = line.strip()

        # 处理翻译行
        if '翻译' in line and ('：' in line or ':' in line):
            # 尝试提取翻译内容
            parts = re.split('[:：]', line, 1)
            if len(parts) > 1:
                translation = parts[1].strip()

        # 处理关键词行
        elif '关键词' in line and ('：' in line or ':' in line):
            # 尝试提取关键词
            parts = re.split('[:：]', line, 1)
            if len(parts) > 1:
                keywords_str = parts[1].strip()
                # 支持多种分隔符：逗号、分号、顿号
                keywords = [
                    kw.strip()
                    for kw in re.split('[,，;；、]', keywords_str)
                    if kw.strip()
                ]

    # 如果没有提取到翻译，尝试从整体内容中提取
    if not translation:
        # 尝试匹配英文句子（简单判断包含英文字母）
        for line in lines:
            if re.search(r'[a-zA-Z]', line) and '关键词' not in line:
                translation = line.strip()
                break

    # 确保翻译结果不为空
    if not translation:
        translation = "翻译失败，请重试"

    # 确保有关键词
    if not keywords:
        keywords = ["未提取到关键词"]

    # 清理关键词中的特殊字符
    keywords = [re.sub(r'[^\w\s\u4e00-\u9fff]', '', kw) for kw in keywords if kw]

    return translation, keywords


def translate_text(text):
    """
    调用通义千问API进行翻译和关键词提取

    Args:
        text (str): 要翻译的中文文本

    Returns:
        dict: 包含translation和keywords的字典
    """
    # 构造API请求消息
    messages = [
        {
            "role": "system",
            "content": "你是一个专业的翻译助手。请将用户输入的中文翻译成自然的英文，并从原文中提取3-5个最重要的关键词。"
        },
        {
            "role": "user",
            "content": f"请将以下中文翻译成英文，并提取关键词：\n{text}\n\n请按以下格式返回：\n翻译：[英文翻译]\n关键词：[关键词1, 关键词2, 关键词3]"
        }
    ]

    # 构造API请求
    headers = {
        "Authorization": f"Bearer {config.QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": config.QWEN_MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        # 发送API请求
        logger.info(f"开始翻译，文本长度: {len(text)}")
        response = requests.post(
            config.QWEN_API_URL,
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()

        # 解析API响应
        result = response.json()

        # 增强的响应验证
        if 'choices' not in result or not result['choices']:
            raise Exception("API返回格式异常")

        if 'message' not in result['choices'][0]:
            raise Exception("API返回格式异常")

        if 'content' not in result['choices'][0]['message']:
            raise Exception("API返回格式异常")

        content = result['choices'][0]['message']['content']

        if not content or not isinstance(content, str):
            raise Exception("翻译内容为空或格式错误")

        # 使用增强的解析函数
        translation, keywords = parse_translation_result(content)

        logger.info(f"翻译成功，提取到 {len(keywords)} 个关键词")
        return {
            "translation": translation,
            "keywords": keywords
        }

    except requests.exceptions.Timeout:
        logger.error("API请求超时")
        raise Exception("翻译服务响应超时，请稍后重试")
    except requests.exceptions.HTTPError as e:
        logger.error(f"API HTTP错误: {e.response.status_code}")
        if e.response.status_code == 401:
            raise Exception("API认证失败，请检查配置")
        elif e.response.status_code == 429:
            raise Exception("API请求过于频繁，请稍后重试")
        else:
            raise Exception("翻译服务暂时不可用")
    except requests.exceptions.RequestException as e:
        logger.error(f"API调用失败: {str(e)}")
        raise Exception("翻译服务连接失败，请稍后重试")
    except Exception as e:
        logger.error(f"翻译处理失败: {str(e)}")
        raise Exception("翻译失败，请稍后重试")


def create_app():
    """
    创建并配置Flask应用

    Returns:
        Flask: 配置好的Flask应用实例
    """
    app = Flask(__name__)

    # 配置应用
    app.config['DEBUG'] = config.FLASK_DEBUG

    # 配置安全响应头
    @app.after_request
    def set_security_headers(response):
        # 防止MIME类型嗅探
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # 防止点击劫持
        response.headers['X-Frame-Options'] = 'DENY'
        # 启用浏览器XSS过滤
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # 内容安全策略
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        # 严格传输安全（仅在生产环境使用HTTPS时启用）
        # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    return app


# 创建应用实例
app = create_app()


@app.route('/')
def index():
    """
    首页路由，返回前端页面

    Returns:
        str: 渲染的HTML页面
    """
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
@rate_limit
def translate():
    """
    翻译接口，处理翻译请求

    Returns:
        JSON: 翻译结果或错误信息
    """
    try:
        # 获取请求参数
        data = request.get_json()

        if not data or 'text' not in data:
            logger.warning("收到缺少text参数的请求")
            return jsonify({"error": "缺少text参数"}), 400

        text = data['text']

        # 使用增强的输入验证
        is_valid, error_message, sanitized_text = validate_and_sanitize_input(text)

        if not is_valid:
            logger.warning(f"输入验证失败: {error_message}")
            return jsonify({"error": error_message}), 400

        # 调用翻译函数
        result = translate_text(sanitized_text)

        return jsonify(result)

    except Exception as e:
        logger.error(f"翻译接口异常: {str(e)}")
        # 不暴露详细的错误信息给客户端
        return jsonify({"error": "翻译失败，请稍后重试"}), 500


@app.errorhandler(404)
def not_found(error):
    """处理404错误"""
    logger.warning(f"404错误: {request.url}")
    return jsonify({"error": "接口不存在"}), 404


@app.errorhandler(500)
def internal_error(error):
    """处理500错误"""
    logger.error(f"500错误: {str(error)}")
    return jsonify({"error": "服务器内部错误"}), 500


@app.errorhandler(429)
def rate_limit_exceeded(error):
    """处理429限流错误"""
    logger.warning(f"429限流错误: {request.remote_addr}")
    return jsonify({"error": "请求过于频繁"}), 429


if __name__ == '__main__':
    # 启动Flask应用
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
