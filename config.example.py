"""
配置文件
请填入您的真实配置信息
"""

# 通义千问API配置
QWEN_API_KEY = "YOUR-API"  # 请替换为您的真实API密钥
QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
QWEN_MODEL = "qwen-plus-2025-07-28"

# Flask应用配置
FLASK_HOST = "0.0.0.0"  # 监听所有网络接口
FLASK_PORT = 5000  # 端口号
FLASK_DEBUG = True  # 调试模式，生产环境应设置为False

# 语音合成API配置
TTS_API_KEY = "YOUR-API"  # 请替换为您的真实API密钥
TTS_API_URL = "https://aiapiv2.pekpik.com/v1"
TTS_MODEL = "tts-1-hd"
TTS_VOICE = "alloy"  # 可选声音: alloy, echo, fable, onyx, nova, shimmer

# 代理配置（可选，如不需要代理可设置为空字符串）
HTTP_PROXY = "http://127.0.0.1:7890"  # 留空表示不使用代理
HTTPS_PROXY = "http://127.0.0.1:7890"  # 留空表示不使用代理
