"""
配置文件示例
复制此文件为config.py，并填入您的真实配置信息
"""

# 通义千问API配置
QWEN_API_KEY = "your_api_key_here"  # 请替换为您的真实API密钥
QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
QWEN_MODEL = "qwen-plus-2025-07-28"

# Flask应用配置
FLASK_HOST = "0.0.0.0"  # 监听所有网络接口
FLASK_PORT = 5000  # 端口号
FLASK_DEBUG = True  # 调试模式，生产环境应设置为False
