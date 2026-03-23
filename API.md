# API文档

## 基础信息

- **Base URL**: `http://localhost:5000` (默认)
- **Content-Type**: `application/json`

## API端点

### 1. 首页

获取应用主页。

**请求**
```
GET /
```

**响应**
- Content-Type: `text/html`
- 返回渲染的HTML页面

---

### 2. 翻译接口

将中文文本翻译为英文,提取关键词,并生成语音。

**请求**
```
POST /translate
```

**请求参数**

| 参数名 | 类型   | 必填 | 描述           | 限制                     |
|--------|--------|------|----------------|--------------------------|
| text   | string | 是   | 要翻译的中文文本 | 长度1-1000字符,必须包含中文 |

**请求示例**

```json
{
  "text": "今天天气很好,我想去公园散步"
}
```

**成功响应**

**HTTP状态码**: `200 OK`

**响应示例**

```json
{
  "translation": "The weather is very nice today, I want to go for a walk in the park",
  "keywords": ["天气", "公园", "散步"],
  "audio_url": "/static/audio/output_20260323_154633.mp3"
}
```

**响应字段说明**

| 字段名     | 类型   | 描述                           |
|------------|--------|--------------------------------|
| translation| string | 英文翻译结果                   |
| keywords   | array  | 提取的关键词列表(3-5个)        |
| audio_url  | string | 生成的语音文件URL              |

---

### 错误响应

#### 1. 参数错误 (400 Bad Request)

**请求参数缺失或无效**

```json
{
  "error": "缺少text参数"
}
```

或

```json
{
  "error": "输入内容不能为空"
}
```

或

```json
{
  "error": "输入内容过长,请限制在1000字以内"
}
```

或

```json
{
  "error": "请输入中文内容"
}
```

或

```json
{
  "error": "输入内容包含不安全的字符"
}
```

---

#### 2. 限流错误 (429 Too Many Requests)

**请求频率超过限制**

```json
{
  "error": "请求过于频繁,请稍后再试"
}
```

或

```json
{
  "error": "请求次数超过限制,请1小时后再试"
}
```

---

#### 3. 服务器错误 (500 Internal Server Error)

**服务器内部错误**

```json
{
  "error": "翻译失败,请稍后重试"
}
```

或

```json
{
  "error": "服务器内部错误"
}
```

---

#### 4. 接口不存在 (404 Not Found)

**请求的接口不存在**

```json
{
  "error": "接口不存在"
}
```

---

## 限流策略

为了防止API滥用,系统实现了限流机制:

| 限制类型   | 限制值       | 说明           |
|------------|--------------|----------------|
| 每分钟请求 | 30次/分钟    | 基于客户端IP   |
| 每小时请求 | 100次/小时   | 基于客户端IP   |

触发限流时,返回 `429 Too Many Requests` 状态码。

---

## 安全特性

### 输入验证

- **长度限制**: 输入文本长度必须在1-1000字符之间
- **内容要求**: 必须包含至少一个中文字符
- **安全过滤**: 自动过滤以下危险内容:
  - `<script>` 标签
  - 事件处理器 (如 `onclick=`)
  - `javascript:` 协议
  - `<iframe>`、`<object>`、`<embed>` 标签

### 安全响应头

所有响应都包含以下安全头:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; media-src 'self' blob:;
```

---

## 使用示例

### cURL示例

```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "今天天气很好"}'
```

### Python示例

```python
import requests
import json

url = "http://localhost:5000/translate"
data = {"text": "今天天气很好"}

response = requests.post(url, json=data)
result = response.json()

print(f"翻译: {result['translation']}")
print(f"关键词: {result['keywords']}")
print(f"音频: {result['audio_url']}")
```

### JavaScript示例

```javascript
const data = {
  text: "今天天气很好"
};

fetch('http://localhost:5000/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(data => {
    console.log('翻译:', data.translation);
    console.log('关键词:', data.keywords);
    console.log('音频:', data.audio_url);
  })
  .catch(error => console.error('错误:', error));
```

---

## 注意事项

1. **API密钥配置**: 使用前请确保在 `config.py` 中正确配置了API密钥
2. **网络连接**: 翻译和语音合成需要访问外部API,请确保网络连接正常
3. **音频文件**: 生成的音频文件保存在服务器端,URL相对路径为 `/static/audio/{filename}`
4. **异步处理**: 翻译和语音合成是同步处理的,大文本可能需要较长等待时间
5. **错误处理**: 客户端应妥善处理各种错误响应

---

## 更新日志

### v1.0.0
- 初始版本
- 支持中文到英文翻译
- 支持关键词提取
- 支持语音合成
- 实现限流机制
- 实现输入验证和安全防护
