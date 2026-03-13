# AI翻译助手

一个基于Flask和通义千问API的智能翻译应用，提供中文到英文的翻译服务，并自动提取关键词。

## 功能特性

- **智能翻译**: 使用通义千问大模型进行高质量的中文到英文翻译
- **关键词提取**: 自动从原文中提取3-5个最重要的关键词
- **简洁界面**: 现代化的Web界面，操作简单直观
- **实时反馈**: 翻译过程中显示加载状态，提供友好的用户体验

## 安全特性

### 输入验证
- 长度限制: 输入文本长度不超过1000字
- 内容验证: 必须包含中文字符
- 安全过滤: 自动过滤恶意脚本和危险字符（如`<script>`、`javascript:`等）

### 限流保护
- 每分钟限制: 每个IP每分钟最多30次请求
- 每小时限制: 每个IP每小时最多100次请求
- 触发限流: 返回HTTP 429状态码

### 错误处理
- 安全响应: 不暴露服务器内部错误详情
- 日志记录: 详细记录错误信息用于调试
- 用户友好: 返回简洁明确的错误提示

### 安全响应头
- `X-Content-Type-Options`: `nosniff` - 防止MIME类型嗅探
- `X-Frame-Options`: `DENY` - 防止点击劫持
- `X-XSS-Protection`: `1; mode=block` - 启用浏览器XSS过滤
- `Content-Security-Policy`: 限制资源加载来源

### 前端安全
- XSS防护: 所有动态内容都经过HTML转义
- 输入验证: 前端和服务端双重验证
- 错误处理: 网络错误和API错误的友好提示
- 防重复点击: 防止用户重复提交请求

## 技术栈

### 后端
- **Flask 3.0.0**: Python Web框架
- **Requests 2.31.0**: HTTP库，用于调用通义千问API
- **通义千问API**: 阿里云大语言模型服务

### 前端
- **HTML5**: 页面结构
- **CSS3**: 样式设计
- **JavaScript (Vanilla)**: 交互逻辑

## 项目结构

```
shixi/
├── app.py                 # Flask应用主文件
├── config.py              # 配置文件（需自行创建）
├── config.example.py      # 配置文件模板
├── requirements.txt       # Python依赖
├── API.md                 # API接口文档
├── CONFIG.md              # 配置说明文档
├── README.md              # 项目说明文档（本文件）
├── templates/
│   └── index.html         # 前端页面模板
└── static/
    ├── css/
    │   └── style.css      # 样式文件
    └── js/
        └── script.js      # JavaScript逻辑
```

## 快速开始

### 环境要求

- Python 3.7 或更高版本
- pip (Python包管理器)
- 通义千问API密钥

### 安装步骤

1. **克隆或下载项目**

```bash
# 如果使用Git
git clone <repository-url>
cd translation
```

2. **创建虚拟环境（推荐）**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置API密钥**

复制配置模板并填入您的API密钥：

```bash
# Windows
copy config.example.py config.py

# Linux/Mac
cp config.example.py config.py
```

编辑`config.py`文件，将`QWEN_API_KEY`替换为您的真实API密钥：

```python
QWEN_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"  # 替换为您的真实密钥
```

5. **获取通义千问API密钥**

如果还没有API密钥，请按以下步骤获取：

1. 访问阿里云官网: https://www.aliyun.com
2. 注册并登录阿里云账号
3. 开通通义千问服务
4. 进入控制台，创建API密钥
5. 复制API密钥到配置文件

6. **启动应用**

```bash
python app.py
```

7. **访问应用**

打开浏览器访问: http://localhost:5000

## 使用说明

### Web界面使用

1. 在输入框中输入要翻译的中文内容
2. 点击"翻译"按钮或按 `Ctrl + Enter` 快捷键
3. 等待翻译结果和关键词显示

### API接口使用

详见 [API.md](API.md) 文档。

**快速示例**:

```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "人工智能正在改变世界"}'
```

**响应示例**:

```json
{
  "translation": "Artificial intelligence is changing the world",
  "keywords": ["人工智能", "改变", "世界"]
}
```

## 配置说明

详细的配置说明请参考 [CONFIG.md](CONFIG.md) 文档。

### 主要配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| QWEN_API_KEY | 通义千问API密钥 | - |
| QWEN_API_URL | API访问地址 | https://dashscope.aliyuncs.com/... |
| QWEN_MODEL | 使用的模型 | qwen-plus-2025-07-28 |
| FLASK_HOST | 服务器地址 | 0.0.0.0 |
| FLASK_PORT | 服务器端口 | 5000 |
| FLASK_DEBUG | 调试模式 | True |

### 开发环境配置

```python
# config.py
FLASK_HOST = "127.0.0.1"  # 仅本地访问
FLASK_DEBUG = True        # 启用调试模式
```

### 生产环境配置

```python
# config.py
FLASK_HOST = "0.0.0.0"    # 允许外部访问
FLASK_DEBUG = False       # 禁用调试模式
```

## 开发指南

### 添加新功能

1. 在`app.py`中添加新的路由和处理函数
2. 在`templates/index.html`中添加UI元素
3. 在`static/js/script.js`中添加前端逻辑
4. 更新API文档（如涉及API变更）

### 运行测试

建议进行以下测试：

1. **正常翻译测试**: 测试各种正常的中文文本
2. **边界测试**: 测试空文本、超长文本等边界情况
3. **错误测试**: 测试缺少参数、错误格式等异常情况
4. **性能测试**: 测试并发请求和响应时间
5. **安全测试**:
   - 测试包含恶意脚本的输入
   - 测试限流功能
   - 验证安全响应头

## 安全建议

1. **保护API密钥**:
   - 不要将`config.py`提交到版本控制系统
   - 生产环境建议使用环境变量存储敏感信息
   - 定期更换API密钥

2. **启用HTTPS**:
   - 生产环境必须使用HTTPS
   - 配置HSTS响应头

3. **监控日志**:
   - 定期检查应用日志
   - 监控异常请求和安全事件

4. **更新依赖**:
   - 定期更新Python依赖包
   - 关注安全漏洞公告

## 常见问题

### 1. API调用失败

**问题**: 提示"翻译服务暂时不可用"

**解决**:
- 检查API密钥是否正确
- 确认API密钥有足够的调用额度
- 检查网络连接是否正常

### 2. 端口被占用

**问题**: 启动失败，提示端口已被占用

**解决**:
- 修改`config.py`中的`FLASK_PORT`为其他端口
- 或者停止占用该端口的程序

### 3. 无法从外部访问

**问题**: 其他设备无法访问应用

**解决**:
- 检查防火墙设置
- 确认`FLASK_HOST`设置为`0.0.0.0`
- 确认网络连接正常

### 4. 触发限流

**问题**: 提示"请求过于频繁"

**解决**:
- 降低请求频率
- 等待限流时间结束后重试

## 版本历史

### v2.0.0 (2025-03-13) - 安全增强版本

- 添加输入验证和过滤机制
- 实现限流保护功能
- 改进错误处理，避免信息泄露
- 增强模型输出解析的健壮性
- 添加安全响应头
- 加强前端XSS防护

### v1.0.0 (2024-03-13) - 初始版本

- 基础翻译功能
- 关键词提取
- Web界面
- RESTful API接口

## 许可证

本项目仅用于技术测试和学习目的。
