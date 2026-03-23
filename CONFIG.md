# 配置说明文档

本文档详细说明AI翻译助手项目的配置项和配置方法。

## 配置文件

项目使用`config.py`作为主配置文件，`config.example.py`作为配置模板。

### 获取配置文件

首次使用时，需要复制配置模板：

```bash
# Windows
copy config.example.py config.py

# Linux/Mac
cp config.example.py config.py
```

## 配置项说明

### 通义千问API配置

#### QWEN_API_KEY

**说明**: 通义千问API的访问密钥

**必填**: 是

**如何获取**:
1. 访问阿里云官网: https://www.aliyun.com
2. 注册并登录阿里云账号
3. 开通通义千问服务
4. 进入控制台，创建API密钥
5. 复制API密钥到配置文件

**示例**:
```python
QWEN_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
```

**注意事项**:
- 不要将真实API密钥提交到版本控制系统
- 定期更换API密钥以保证安全
- 确保API密钥有足够的调用额度

#### QWEN_API_URL

**说明**: 通义千问API的访问地址

**必填**: 否（有默认值）

**默认值**: `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

**修改建议**: 一般不需要修改，除非有特殊需求

#### QWEN_MODEL

**说明**: 使用的通义千问模型名称

**必填**: 否（有默认值）

**默认值**: `qwen-plus-2025-07-28`

**可选模型**:
- `qwen-plus-2025-07-28`: 最新增强版模型（推荐）
- `qwen-plus`: 通用增强版模型
- `qwen-turbo`: 高性能快速版模型
- `qwen-max`: 最强能力版模型

**修改建议**: 根据项目需求和预算选择合适的模型

### Flask应用配置

#### FLASK_HOST

**说明**: Flask服务器监听的网络地址

**必填**: 否（有默认值）

**默认值**: `0.0.0.0`

**可选值**:
- `0.0.0.0`: 监听所有网络接口（可从外部访问）
- `127.0.0.1`: 仅监听本地（仅本机访问）

**示例**:
```python
FLASK_HOST = "0.0.0.0"  # 允许外部访问
FLASK_HOST = "127.0.0.1"  # 仅本地访问
```

#### FLASK_PORT

**说明**: Flask服务器监听的端口号

**必填**: 否（有默认值）

**默认值**: `5000`

**修改建议**:
- 如果5000端口被占用，可以修改为其他端口
- 确保使用的端口未被其他程序占用

**示例**:
```python
FLASK_PORT = 5000  # 默认端口
FLASK_PORT = 8000  # 自定义端口
```

#### FLASK_DEBUG

**说明**: 是否启用调试模式

**必填**: 否（有默认值）

**默认值**: `True`

**可选值**:
- `True`: 启用调试模式（开发环境）
- `False`: 禁用调试模式（生产环境）

**调试模式特点**:
- 代码修改后自动重启服务器
- 显示详细的错误信息
- 提供调试工具

**生产环境建议**:
```python
FLASK_DEBUG = False  # 生产环境必须设置为False
```

### 安全配置（在app.py中配置）

#### 限流配置

**说明**: 防止API滥用，限制每个IP的请求频率

**配置位置**: `app.py` 中的 `RATE_LIMIT_CONFIG`

**默认配置**:
```python
RATE_LIMIT_CONFIG = {
    'max_requests_per_minute': 30,  # 每分钟最多30次请求
    'max_requests_per_hour': 100    # 每小时最多100次请求
}
```

**自定义配置**:
在`app.py`中修改`RATE_LIMIT_CONFIG`字典的值：

```python
# 更严格的限流
RATE_LIMIT_CONFIG = {
    'max_requests_per_minute': 10,  # 每分钟最多10次请求
    'max_requests_per_hour': 50     # 每小时最多50次请求
}

# 更宽松的限流
RATE_LIMIT_CONFIG = {
    'max_requests_per_minute': 60,  # 每分钟最多60次请求
    'max_requests_per_hour': 300    # 每小时最多300次请求
}
```

#### 超时配置

**说明**: API请求的超时时间

**配置位置**: `app.py` 中 `translate_text()` 函数的 `timeout` 参数

**默认值**: 30秒

**自定义配置**:
```python
response = requests.post(
    config.QWEN_API_URL,
    headers=headers,
    json=data,
    timeout=60  # 修改为60秒
)
```

#### 安全响应头配置

**说明**: 设置HTTP安全响应头以增强安全性

**配置位置**: `app.py` 中 `set_security_headers()` 函数

**默认配置**:
```python
response.headers['X-Content-Type-Options'] = 'nosniff'
response.headers['X-Frame-Options'] = 'DENY'
response.headers['X-XSS-Protection'] = '1; mode=block'
response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
```

**自定义配置**:
```python
# 更严格的CSP策略
response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self';"

# 启用HSTS（仅在使用HTTPS时）
response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
```

### 输入验证配置

#### 文本长度限制

**说明**: 输入文本的最大长度

**配置位置**: `app.py` 中 `validate_and_sanitize_input()` 函数

**默认值**: 1000字

**自定义配置**:
```python
if len(text) > 2000:  # 修改为2000字
    return False, "输入内容过长，请限制在2000字以内", ""
```

#### 危险字符过滤

**说明**: 过滤潜在危险的字符序列

**配置位置**: `app.py` 中 `validate_and_sanitize_input()` 函数的 `dangerous_patterns`

**默认模式**:
```python
dangerous_patterns = [
    r'<script[^>]*>.*?</script>',  # 脚本标签
    r'on\w+\s*=',  # 事件处理器
    r'javascript:',  # JavaScript协议
    r'<iframe',  # iframe标签
    r'<object',  # object标签
    r'<embed',  # embed标签
]
```

**自定义配置**:
可以添加或修改过滤模式：
```python
dangerous_patterns = [
    r'<script[^>]*>.*?</script>',
    r'on\w+\s*=',,
    r'javascript:',
    r'<iframe',
    r'<object',
    r'<embed',
    r'<link',  # 添加link标签过滤
    r'<meta',  # 添加meta标签过滤
]
```

## 完整配置示例

### 开发环境配置

```python
"""
开发环境配置
"""

# 通义千问API配置
QWEN_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
QWEN_MODEL = "qwen-plus-2025-07-28"

# Flask应用配置
FLASK_HOST = "127.0.0.1"  # 仅本地访问
FLASK_PORT = 5000
FLASK_DEBUG = True  # 启用调试模式
```

### 生产环境配置

```python
"""
生产环境配置
"""

# 通义千问API配置
QWEN_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
QWEN_MODEL = "qwen-plus-2025-07-28"

# Flask应用配置
FLASK_HOST = "0.0.0.0"  # 允许外部访问
FLASK_PORT = 5000
FLASK_DEBUG = False  # 禁用调试模式
```

### 高安全配置

```python
"""
高安全配置
"""

# 通义千问API配置
QWEN_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
QWEN_MODEL = "qwen-plus-2025-07-28"

# Flask应用配置
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = False

# 需要在app.py中额外配置：
# - 更严格的限流
# - 更短的超时时间
# - 更严格的CSP策略
# - 启用HSTS
```

## 环境变量配置（推荐）

使用环境变量配置可以增强安全性，避免敏感信息泄露。

### 设置环境变量

**Windows**:
```bash
# 临时设置
set QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
set FLASK_PORT=8000

# 永久设置（系统环境变量）
# 右键"此电脑" -> 属性 -> 高级系统设置 -> 环境变量
```

**Linux/Mac**:
```bash
# 临时设置
export QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
export FLASK_PORT=8000

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx' >> ~/.bashrc
echo 'export FLASK_PORT=8000' >> ~/.bashrc
source ~/.bashrc
```

### 使用.env文件（推荐）

创建`.env`文件（记得添加到`.gitignore`）：

```bash
# .env
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
QWEN_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
QWEN_MODEL=qwen-plus-2025-07-28
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
```

安装`python-dotenv`包：

```bash
pip install python-dotenv
```

在代码中加载环境变量：

```python
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

# 读取配置
QWEN_API_KEY = os.getenv('QWEN_API_KEY', '')
QWEN_API_URL = os.getenv('QWEN_API_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions')
QWEN_MODEL = os.getenv('QWEN_MODEL', 'qwen-plus-2025-07-28')
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
```

## 配置验证

配置完成后，可以运行以下命令验证配置是否正确：

```bash
python -c "import config; print('API Key:', config.QWEN_API_KEY[:10] + '...'); print('Model:', config.QWEN_MODEL); print('Port:', config.FLASK_PORT)"
```

输出示例：
```
API Key: sk-xxxxxxx...
Model: qwen-plus-2025-07-28
Port: 5000
```

## 常见问题

### 1. API密钥无效

**问题**: 提示"API调用失败"或"API认证失败"

**解决**:
- 检查API密钥是否正确复制（注意不要有多余空格）
- 确认API密钥是否已激活
- 检查API密钥是否有足够的调用额度
- 确认API密钥是否已开通通义千问服务
- 查看阿里云控制台的API密钥状态

### 2. 端口被占用

**问题**: 启动失败，提示端口已被占用

**解决**:
- 修改`config.py`中的`FLASK_PORT`为其他端口
- 或者停止占用该端口的程序

**Windows查找占用端口的进程**:
```bash
netstat -ano | findstr :5000
taskkill /PID <进程ID> /F
```

**Linux/Mac查找占用端口的进程**:
```bash
lsof -i :5000
kill -9 <进程ID>
```

### 3. 无法从外部访问

**问题**: 其他设备无法访问应用

**解决**:
- 检查防火墙设置，允许5000端口入站
- 确认`FLASK_HOST`设置为`0.0.0.0`
- 确认网络连接正常
- 检查云服务器的安全组设置（如果使用云服务器）

### 4. 触发限流

**问题**: 提示"请求过于频繁"

**解决**:
- 降低请求频率
- 等待限流时间结束后重试
- 调整`app.py`中的限流配置

### 5. 翻译速度慢

**问题**: API响应时间过长

**解决**:
- 检查网络连接
- 考虑使用更快的模型（如`qwen-turbo`）
- 增加超时时间配置
- 检查通义千问API服务状态

## 安全建议

### 基础安全

1. **不要提交配置文件**: 将`config.py`和`.env`添加到`.gitignore`
2. **定期更换密钥**: 定期更换API密钥以保证安全
3. **使用环境变量**: 生产环境建议使用环境变量存储敏感信息
4. **限制调试模式**: 生产环境必须禁用调试模式

### 高级安全

5. **监控API调用**: 定期检查API调用日志，发现异常及时处理
6. **启用HTTPS**: 生产环境必须使用HTTPS
7. **配置HSTS**: 启用HTTP严格传输安全
8. **使用反向代理**: 使用Nginx等反向代理服务器
9. **实施访问控制**: 添加用户认证和授权机制
10. **日志审计**: 记录所有API请求和响应，定期审计

### .gitignore配置

确保`.gitignore`文件包含以下内容：

```gitignore
# 配置文件
config.py
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 日志
*.log

# 临时文件
*.tmp
.DS_Store
```

## 配置文件模板

始终保留`config.example.py`作为配置模板，方便其他开发者快速配置：

```python
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
```

## 性能优化建议

### 1. 缓存翻译结果

对于相同的输入，可以缓存翻译结果以减少API调用：

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def translate_text_cached(text):
    return translate_text(text)
```

### 2. 异步处理

使用异步处理提高并发性能：

```python
import asyncio
import aiohttp

async def translate_text_async(text):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            config.QWEN_API_URL,
            headers=headers,
            json=data
        ) as response:
            return await response.json()
```

### 3. 连接池

使用连接池减少连接开销：

```python
session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=100))
```

## 监控和日志

### 日志配置

在`app.py`中配置日志：

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 添加文件日志（自动轮转）
file_handler = RotatingFileHandler(
    'app.log',
    maxBytes=1024*1024,  # 1MB
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logging.getLogger().addHandler(file_handler)
```

### 监控指标

建议监控以下指标：
- API请求成功率
- 平均响应时间
- 限流触发次数
- 错误类型分布
- 活跃用户数

## 部署建议

### 使用Gunicorn部署

生产环境建议使用Gunicorn：

```bash
pip install gunicorn

# 启动
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用Docker部署

创建`Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建和运行：

```bash
docker build -t ai-translator .
docker run -p 5000:5000 --env-file .env ai-translator
```

## 相关文档

- [API接口文档](API.md) - 详细的API使用说明
- [README.md](README.md) - 项目概述和快速开始
- 通义千问官方文档: https://help.aliyun.com/zh/dashscope/

