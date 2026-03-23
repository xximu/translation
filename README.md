# AI翻译助手

一个基于Flask的智能翻译应用,提供中文到英文的翻译功能,同时自动提取关键词并生成英文语音。

## 功能特性

- **智能翻译**: 使用通义千问API进行高质量的中文到英文翻译
- **关键词提取**: 自动从原文中提取3-5个最重要的关键词
- **语音合成**: 将翻译结果转换为英文语音,支持在线播放
- **输入验证**: 完善的输入验证和安全防护机制
- **限流保护**: 防止API滥用的请求限流机制
- **安全防护**: 多层安全防护,包括XSS防护、输入清理等

## 技术栈

- **后端**: Flask (Python Web框架)
- **AI翻译**: 通义千问API (阿里云)
- **语音合成**: OpenAI兼容的TTS API
- **前端**: 原生HTML/CSS/JavaScript

## 项目结构

```
translation-master/
├── app.py                 # Flask应用主文件
├── config.py             # 配置文件(需自行创建)
├── config.example.py     # 配置文件示例
├── templates/
│   └── index.html        # 前端页面
├── static/
│   ├── css/
│   │   └── style.css     # 样式文件
│   ├── js/
│   │   └── script.js     # 前端脚本
│   └── audio/            # 生成的音频文件目录
└── README.md             # 项目说明文档
```

## 快速开始

### 1. 环境要求

- Python 3.7+
- pip (Python包管理器)

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装所需依赖:

```bash
pip install flask requests openai
```

### 3. 配置环境

复制配置文件示例并填入您的API密钥:

```bash
cp config.example.py config.py
```

编辑 `config.py` 文件,填入以下配置:

```python
# 通义千问API配置
QWEN_API_KEY = "YOUR-API-KEY"  # 替换为您的通义千问API密钥
QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
QWEN_MODEL = "qwen-plus-2025-07-28"

# 语音合成API配置
TTS_API_KEY = "YOUR-TTS-API-KEY"  # 替换为您的TTS API密钥
TTS_API_URL = "https://aiapiv2.pekpik.com/v1"
TTS_MODEL = "tts-1-hd"
TTS_VOICE = "alloy"  # 可选: alloy, echo, fable, onyx, nova, shimmer

# Flask应用配置
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True  # 生产环境请设置为False

# 代理配置(可选)
HTTP_PROXY = ""  # 如需代理,填写代理地址,否则留空
HTTPS_PROXY = ""
```

### 4. 启动应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

### 5. 使用应用

打开浏览器访问 `http://localhost:5000`,在页面中输入中文内容,点击"翻译"按钮即可获得翻译结果、关键词和语音播放。

## API文档

详细的API文档请参考 [API.md](./API.md)

## 安全特性

### 输入验证
- 内容长度限制(1000字以内)
- 必须包含中文字符
- 过滤危险字符序列(脚本标签、事件处理器等)

### 限流保护
- 每分钟最多30次请求
- 每小时最多100次请求

### 安全响应头
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy: 严格的CSP策略

## 注意事项

1. **API密钥安全**: 请勿将包含真实API密钥的config.py文件提交到版本控制系统
2. **生产环境部署**: 生产环境部署时,请将 `FLASK_DEBUG` 设置为 `False`
3. **代理配置**: 如果您的网络环境需要访问外网,请配置代理
4. **音频文件**: 生成的音频文件保存在 `static/audio` 目录下,建议定期清理

## 常见问题

### Q: 提示"API认证失败"
A: 请检查config.py中的API密钥是否正确配置

### Q: 提示"请求过于频繁"
A: 您已触发限流机制,请稍后再试

### Q: 语音无法播放
A: 请检查TTS_API_KEY是否正确配置,以及网络连接是否正常

### Q: 翻译结果不准确
A: 翻译质量取决于AI模型,可以尝试调整prompt或更换模型

## 许可证

本项目为技术测试项目,仅供学习和研究使用。

## 联系方式

如有问题或建议,欢迎提出Issue。
