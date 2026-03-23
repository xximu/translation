# API接口文档

## 概述

AI翻译助手提供了一个RESTful API接口，用于将中文翻译成英文并提取关键词。

## 基础信息

- **Base URL**: `http://localhost:5000`
- **Content-Type**: `application/json`
- **字符编码**: UTF-8

## 安全特性

### 输入验证
- **长度限制**: 输入文本长度不超过1000字
- **内容验证**: 必须包含中文字符
- **安全过滤**: 自动过滤恶意脚本和危险字符（如`<script>`、`javascript:`等）

### 限流保护
- **每分钟限制**: 每个IP每分钟最多30次请求
- **每小时限制**: 每个IP每小时最多100次请求
- **触发限流**: 返回HTTP 429状态码

### 错误处理
- **安全响应**: 不暴露服务器内部错误详情
- **日志记录**: 详细记录错误信息用于调试
- **用户友好**: 返回简洁明确的错误提示

### 安全响应头
- **X-Content-Type-Options**: `nosniff` - 防止MIME类型嗅探
- **X-Frame-Options**: `DENY` - 防止点击劫持
- **X-XSS-Protection**: `1; mode=block` - 启用浏览器XSS过滤
- **Content-Security-Policy**: 限制资源加载来源

### 前端安全
- **XSS防护**: 所有动态内容都经过HTML转义
- **输入验证**: 前端和服务端双重验证
- **错误处理**: 网络错误和API错误的友好提示
- **防重复点击**: 防止用户重复提交请求

## 接口列表

### 1. 翻译接口

将中文翻译成英文并提取关键词。

#### 请求信息

- **URL**: `/translate`
- **方法**: `POST`
- **Content-Type**: `application/json`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| text | string | 是 | 要翻译的中文文本，长度不超过1000字 | "人工智能正在改变世界" |

#### 请求示例

```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "人工智能正在改变世界"}'
```

#### 响应格式

**成功响应** (HTTP 200)

```json
{
  "translation": "Artificial intelligence is changing the world",
  "keywords": ["人工智能", "改变", "世界"]
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| translation | string | 英文翻译结果 |
| keywords | array | 从原文中提取的关键词列表 |

**错误响应** (HTTP 400)

```json
{
  "error": "缺少text参数"
}
```

```json
{
  "error": "输入内容不能为空"
}
```

```json
{
  "error": "输入内容过长，请限制在1000字以内"
}
```

```json
{
  "error": "请输入中文内容"
}
```

```json
{
  "error": "输入内容包含不安全的字符"
}
```

**错误响应** (HTTP 429)

```json
{
  "error": "请求过于频繁，请稍后再试"
}
```

```json
{
  "error": "请求次数超过限制，请1小时后再试"
}
```

**错误响应** (HTTP 500)

```json
{
  "error": "翻译失败，请稍后重试"
}
```

```json
{
  "error": "翻译服务响应超时，请稍后重试"
}
```

```json
{
  "error": "翻译服务暂时不可用"
}
```

#### 错误码说明

| HTTP状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 接口不存在 |
| 429 | 请求过于频繁（触发限流） |
| 500 | 服务器内部错误 |

## 使用示例

### JavaScript (fetch)

```javascript
async function translateText(text) {
  const response = await fetch('http://localhost:5000/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: text })
  });

  const result = await response.json();

  if (response.ok) {
    console.log('翻译结果:', result.translation);
    console.log('关键词:', result.keywords);
  } else {
    console.error('翻译失败:', result.error);
  }
}

// 使用示例
translateText('人工智能正在改变世界');
```

### JavaScript (async/await with error handling)

```javascript
async function translateWithErrorHandling(text) {
  try {
    const response = await fetch('http://localhost:5000/translate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: text })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || '翻译失败');
    }

    const result = await response.json();
    return {
      success: true,
      translation: result.translation,
      keywords: result.keywords
    };

  } catch (error) {
    console.error('翻译错误:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

// 使用示例
translateWithErrorHandling('人工智能正在改变世界')
  .then(result => {
    if (result.success) {
      console.log('翻译:', result.translation);
      console.log('关键词:', result.keywords);
    } else {
      console.error('失败:', result.error);
    }
  });
```

### Python (requests)

```python
import requests

def translate_text(text):
    url = 'http://localhost:5000/translate'
    data = {'text': text}

    response = requests.post(url, json=data)
    result = response.json()

    if response.status_code == 200:
        print('翻译结果:', result['translation'])
        print('关键词:', result['keywords'])
    else:
        print('翻译失败:', result['error'])

# 使用示例
translate_text('人工智能正在改变世界')
```

### Python (with timeout and retry)

```python
import requests
import time

def translate_with_retry(text, max_retries=3, timeout=30):
    url = 'http://localhost:5000/translate'
    data = {'text': text}

    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                json=data,
                timeout=timeout
            )
            result = response.json()

            if response.status_code == 200:
                return result['translation'], result['keywords']
            elif response.status_code == 429:
                # 触发限流，等待后重试
                wait_time = (attempt + 1) * 2
                print(f'触发限流，等待{wait_time}秒后重试...')
                time.sleep(wait_time)
            else:
                raise Exception(result['error'])

        except requests.exceptions.Timeout:
            print(f'请求超时，第{attempt + 1}次重试...')
        except requests.exceptions.RequestException as e:
            print(f'请求失败: {e}')

    raise Exception('翻译失败，已达到最大重试次数')

# 使用示例
try:
    translation, keywords = translate_with_retry('人工智能正在改变世界')
    print('翻译:', translation)
    print('关键词:', keywords)
except Exception as e:
    print('错误:', e)
```

### cURL

```bash
# 基本请求
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "人工智能正在改变世界"}'

# 格式化输出
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "人工智能正在改变世界"}' \
  | jq .

# 保存结果到文件
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "人工智能正在改变世界"}' \
  -o result.json
```

### Node.js (axios)

```javascript
const axios = require('axios');

async function translateText(text) {
  try {
    const response = await axios.post(
      'http://localhost:5000/translate',
      { text: text },
      {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 30000
      }
    );

    console.log('翻译结果:', response.data.translation);
    console.log('关键词:', response.data.keywords);
    return response.data;

  } catch (error) {
    if (error.response) {
      console.error('翻译失败:', error.response.data.error);
    } else if (error.request) {
      console.error('网络错误:', error.message);
    } else {
      console.error('错误:', error.message);
    }
    throw error;
  }
}

// 使用示例
translateText('人工智能正在改变世界')
  .then(result => {
    console.log('成功:', result);
  })
  .catch(error => {
    console.error('失败:', error);
  });
```

### Java (OkHttp)

```java
import okhttp3.*;
import com.google.gson.Gson;
import java.io.IOException;

public class Translator {
    private static final String API_URL = "http://localhost:5000/translate";
    private static final MediaType JSON = MediaType.get("application/json; charset=utf-8");

    public static void main(String[] args) {
        translate("人工智能正在改变世界");
    }

    public static void translate(String text) {
        OkHttpClient client = new OkHttpClient();

        // 构建请求体
        RequestBody body = RequestBody.create(
            "{\"text\":\"" + text + "\"}",
            JSON
        );

        Request request = new Request.Builder()
            .url(API_URL)
            .post(body)
            .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful()) {
                String responseBody = response.body().string();
                Gson gson = new Gson();
                TranslationResult result = gson.fromJson(responseBody, TranslationResult.class);
                System.out.println("翻译结果: " + result.translation);
                System.out.println("关键词: " + String.join(", ", result.keywords));
            } else {
                String errorBody = response.body().string();
                System.err.println("翻译失败: " + errorBody);
            }
        } catch (IOException e) {
            System.err.println("请求错误: " + e.getMessage());
        }
    }

    static class TranslationResult {
        String translation;
        String[] keywords;
    }
}
```

### Go (http)

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "time"
)

type TranslationRequest struct {
    Text string `json:"text"`
}

type TranslationResponse struct {
    Translation string   `json:"translation"`
    Keywords    []string `json:"keywords"`
    Error       string   `json:"error,omitempty"`
}

func translate(text string) (*TranslationResponse, error) {
    // 创建请求体
    requestBody := TranslationRequest{Text: text}
    jsonData, err := json.Marshal(requestBody)
    if err != nil {
        return nil, err
    }

    // 创建HTTP客户端
    client := &http.Client{Timeout: 30 * time.Second}

    // 发送请求
    resp, err := client.Post(
        "http://localhost:5000/translate",
        "application/json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    // 读取响应
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    // 解析响应
    var result TranslationResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }

    if resp.StatusCode != http.StatusOK {
        return &result, fmt.Errorf("API错误: %s", result.Error)
    }

    return &result, nil
}

func main() {
    result, err := translate("人工智能正在改变世界")
    if err != nil {
        fmt.Println("错误:", err)
        return
    }

    fmt.Println("翻译结果:", result.Translation)
    fmt.Println("关键词:", result.Keywords)
}
```

### PHP (cURL)

```php
<?php

function translateText($text) {
    $url = 'http://localhost:5000/translate';
    $data = json_encode(['text' => $text]);

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Content-Length: ' . strlen($data)
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($error) {
        throw new Exception("请求错误: " . $error);
    }

    $result = json_decode($response, true);

    if ($httpCode !== 200) {
        throw new Exception($result['error'] ?? '翻译失败');
    }

    return $result;
}

// 使用示例
try {
    $result = translateText('人工智能正在改变世界');
    echo "翻译结果: " . $result['translation'] . "\n";
    echo "关键词: " . implode(', ', $result['keywords']) . "\n";
} catch (Exception $e) {
    echo "错误: " . $e->getMessage() . "\n";
}
?>
```

## 注意事项

1. **API密钥配置**: 确保在`config.py`中正确配置了通义千问API密钥
2. **网络连接**: 确保服务器可以访问通义千问API服务
3. **文本长度**: 输入文本长度限制为1000字，且必须包含中文字符
4. **错误处理**: 客户端应正确处理各种错误情况，特别是限流错误（HTTP 429）
5. **超时设置**: API请求超时时间为30秒
6. **安全提示**:
   - 所有输入都会经过严格的安全验证和过滤
   - 前端显示的所有内容都经过XSS防护处理
   - 建议在生产环境启用HTTPS并配置HSTS响应头
   - 定期检查日志以监控异常请求和安全事件

## 最佳实践

### 1. 错误处理

**建议**:
- 始终检查HTTP状态码
- 处理各种可能的错误情况
- 提供用户友好的错误提示
- 实现适当的重试机制

**示例**:
```python
def safe_translate(text):
    try:
        response = requests.post(
            'http://localhost:5000/translate',
            json={'text': text},
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # 触发限流，等待后重试
            time.sleep(5)
            return safe_translate(text)
        else:
            error_data = response.json()
            raise Exception(error_data.get('error', '未知错误'))

    except requests.exceptions.Timeout:
        raise Exception('请求超时')
    except requests.exceptions.RequestException as e:
        raise Exception(f'网络错误: {str(e)}')
```

### 2. 限流处理

**建议**:
- 监控剩余请求次数
- 实现指数退避重试
- 在接近限流时降低请求频率
- 使用队列管理批量请求

**示例**:
```python
import time
import random

def translate_with_backoff(text, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                'http://localhost:5000/translate',
                json={'text': text},
                timeout=30
            )

            if response.status_code == 429:
                # 指数退避
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f'触发限流，等待{wait_time:.2f}秒...')
                time.sleep(wait_time)
                continue

            return response.json()

        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

    raise Exception('翻译失败')
```

### 3. 缓存策略

**建议**:
- 对相同的输入进行缓存
- 设置合理的缓存过期时间
- 使用内存缓存或Redis
- 实现缓存预热

**示例**:
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_translate(text_hash):
    # 实际翻译逻辑
    return translate_text(text_hash)

def translate_with_cache(text):
    # 使用哈希作为缓存键
    text_hash = hashlib.md5(text.encode()).hexdigest()
    return cached_translate(text_hash)
```

### 4. 批量处理

**建议**:
- 对于大量文本，使用批量处理
- 控制并发请求数量
- 实现请求队列
- 记录处理进度

**示例**:
```python
from concurrent.futures import ThreadPoolExecutor
import threading

def batch_translate(texts, max_workers=5):
    results = []
    lock = threading.Lock()

    def translate_and_store(text):
        try:
            result = translate_text(text)
            with lock:
                results.append({'text': text, 'result': result, 'status': 'success'})
        except Exception as e:
            with lock:
                results.append({'text': text, 'error': str(e), 'status': 'failed'})

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(translate_and_store, texts)

    return results

# 使用示例
texts = ['文本1', '文本2', '文本3', '文本4', '文本5']
results = batch_translate(texts)
```

### 5. 日志记录

**建议**:
- 记录所有API请求和响应
- 记录错误和异常
- 使用结构化日志
- 定期分析日志

**示例**:
```python
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def translate_with_logging(text):
    logger.info(f'开始翻译: {text[:50]}...')

    try:
        response = requests.post(
            'http://localhost:5000/translate',
            json={'text': text},
            timeout=30
        )

        logger.info(f'请求状态码: {response.status_code}')

        if response.status_code == 200:
            result = response.json()
            logger.info(f'翻译成功: {result["translation"][:50]}...')
            return result
        else:
            error_data = response.json()
            logger.error(f'翻译失败: {error_data}')
            raise Exception(error_data.get('error', '未知错误'))

    except Exception as e:
        logger.error(f'翻译异常: {str(e)}', exc_info=True)
        raise
```

### 6. 性能监控

**建议**:
- 监控响应时间
- 监控成功率
- 监控限流触发次数
- 设置告警阈值

**示例**:
```python
import time
from collections import defaultdict

class APIMonitor:
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'count': 0,
            'success': 0,
            'failure': 0,
            'total_time': 0
        })

    def record_request(self, endpoint, success, duration):
        self.metrics[endpoint]['count'] += 1
        self.metrics[endpoint]['total_time'] += duration
        if success:
            self.metrics[endpoint]['success'] += 1
        else:
            self.metrics[endpoint]['failure'] += 1

    def get_stats(self, endpoint):
        m = self.metrics[endpoint]
        if m['count'] == 0:
            return None
        return {
            'count': m['count'],
            'success_rate': m['success'] / m['count'],
            'avg_time': m['total_time'] / m['count']
        }

monitor = APIMonitor()

def monitored_translate(text):
    start_time = time.time()
    try:
        result = translate_text(text)
        duration = time.time() - start_time
        monitor.record_request('/translate', True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        monitor.record_request('/translate', False, duration)
        raise
```

## 性能优化

### 1. 连接池

使用连接池减少连接开销:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 创建session
session = requests.Session()

# 配置重试策略
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

# 配置适配器
adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=10,
    pool_maxsize=100
)

session.mount("http://", adapter)
session.mount("https://", adapter)

# 使用session
response = session.post(
    'http://localhost:5000/translate',
    json={'text': '测试文本'},
    timeout=30
)
```

### 2. 异步请求

使用异步处理提高并发性能:

```python
import asyncio
import aiohttp

async def async_translate(text, session):
    try:
        async with session.post(
            'http://localhost:5000/translate',
            json={'text': text},
            timeout=30
        ) as response:
            return await response.json()
    except Exception as e:
        return {'error': str(e)}

async def batch_async_translate(texts):
    async with aiohttp.ClientSession() as session:
        tasks = [async_translate(text, session) for text in texts]
        return await asyncio.gather(*tasks)

# 使用示例
texts = ['文本1', '文本2', '文本3']
results = asyncio.run(batch_async_translate(texts))
```

### 3. 请求合并

对于相似的请求，可以考虑合并处理:

```python
from collections import defaultdict

class BatchTranslator:
    def __init__(self, batch_size=5, wait_time=2):
        self.batch_size = batch_size
        self.wait_time = wait_time
        self.queue = []
        self.timer = None

    def add_request(self, text, callback):
        self.queue.append({'text': text, 'callback': callback})

        if len(self.queue) >= self.batch_size:
            self.process_batch()
        elif self.timer is None:
            self.timer = threading.Timer(self.wait_time, self.process_batch)
            self.timer.start()

    def process_batch(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

        if not self.queue:
            return

        batch = self.queue[:self.batch_size]
        self.queue = self.queue[self.batch_size:]

        # 批量处理
        for item in batch:
            try:
                result = translate_text(item['text'])
                item['callback'](result, None)
            except Exception as e:
                item['callback'](None, e)

        # 如果还有剩余请求，继续处理
        if self.queue:
            self.process_batch()
```

## 故障排查

### 常见问题诊断

```python
def diagnose_translation(text):
    print("=== 诊断翻译问题 ===")
    print(f"输入文本: {text}")
    print(f"文本长度: {len(text)}")

    # 检查输入验证
    if not text:
        print("❌ 错误: 文本为空")
        return

    if len(text) > 1000:
        print("❌ 错误: 文本过长")
        return

    # 检查网络连接
    import socket
    try:
        socket.create_connection(("localhost", 5000), timeout=5)
        print("✅ 网络连接正常")
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        return

    # 尝试翻译
    try:
        response = requests.post(
            'http://localhost:5000/translate',
            json={'text': text},
            timeout=30
        )

        print(f"HTTP状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ 翻译成功")
            print(f"翻译结果: {result.get('translation', 'N/A')}")
            print(f"关键词: {result.get('keywords', 'N/A')}")
        else:
            error_data = response.json()
            print(f"❌ 翻译失败: {error_data.get('error', '未知错误')}")

    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

# 使用示例
diagnose_translation("人工智能正在改变世界")
```

## 相关文档

- [README.md](README.md) - 项目概述和快速开始
- [CONFIG.md](CONFIG.md) - 配置说明文档
- 通义千问官方文档: https://help.aliyun.com/zh/dashscope/

## 测试建议

1. **正常翻译测试**: 测试各种正常的中文文本
2. **边界测试**: 测试空文本、超长文本等边界情况
3. **错误测试**: 测试缺少参数、错误格式等异常情况
4. **性能测试**: 测试并发请求和响应时间
5. **网络测试**: 测试网络异常情况的处理
6. **安全测试**:
   - 测试包含恶意脚本的输入（如`<script>alert('xss')</script>`）
   - 测试限流功能（快速发送多次请求）
   - 测试SQL注入尝试
   - 测试XSS攻击向量
   - 验证安全响应头是否正确设置

## 版本历史

- **v2.0.0** (2025-03-13): 安全增强版本
  - 添加输入验证和过滤机制
  - 实现限流保护功能
  - 改进错误处理，避免信息泄露
  - 增强模型输出解析的健壮性
  - 添加安全响应头
  - 加强前端XSS防护
- **v1.0.0** (2024-03-13): 初始版本
