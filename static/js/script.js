/**
 * AI翻译助手 - JavaScript逻辑
 * 处理前端交互和API调用
 */

// 获取DOM元素
const inputText = document.getElementById('input-text');
const translateBtn = document.getElementById('translate-btn');
const translationResult = document.getElementById('translation-result');
const keywordsResult = document.getElementById('keywords-result');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');

/**
 * 显示加载状态
 */
function showLoading() {
    loading.classList.remove('hidden');
    translateBtn.disabled = true;
    translateBtn.textContent = '翻译中...';
}

/**
 * 隐藏加载状态
 */
function hideLoading() {
    loading.classList.add('hidden');
    translateBtn.disabled = false;
    translateBtn.textContent = '翻译';
}

/**
 * 显示错误消息
 * @param {string} message - 错误消息
 */
function showError(message) {
    // 验证错误消息
    if (!message || typeof message !== 'string') {
        message = '发生未知错误';
    }

    // 转义错误消息以防止XSS
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

/**
 * 隐藏错误消息
 */
function hideError() {
    errorMessage.classList.add('hidden');
}

/**
 * 显示翻译结果
 * @param {string} translation - 翻译结果
 * @param {Array} keywords - 关键词数组
 */
function showResult(translation, keywords) {
    // 验证输入参数
    if (!translation || typeof translation !== 'string') {
        translation = '翻译结果为空';
    }

    if (!Array.isArray(keywords) || keywords.length === 0) {
        keywords = ['未提取到关键词'];
    }

    // 显示翻译结果
    translationResult.innerHTML = `<p>${escapeHtml(translation)}</p>`;

    // 显示关键词
    keywordsResult.innerHTML = keywords.map(keyword =>
        `<span class="keyword-tag">${escapeHtml(keyword)}</span>`
    ).join('');
}

/**
 * HTML转义，防止XSS攻击
 * @param {string} text - 要转义的文本
 * @returns {string} 转义后的文本
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * 验证输入
 * @returns {boolean} 输入是否有效
 */
function validateInput() {
    const text = inputText.value.trim();

    if (!text) {
        showError('请输入要翻译的中文内容');
        return false;
    }

    if (text.length > 1000) {
        showError('输入内容过长，请限制在1000字以内');
        return false;
    }

    return true;
}

/**
 * 调用翻译API
 * @param {string} text - 要翻译的文本
 * @returns {Promise} API调用Promise
 */
async function translateAPI(text) {
    try {
        const response = await fetch('/translate', {
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

        return response.json();
    } catch (error) {
        // 网络错误处理
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('网络连接失败，请检查网络设置');
        }
        throw error;
    }
}

/**
 * 处理翻译按钮点击事件
 */
async function handleTranslate() {
    // 防止重复点击
    if (translateBtn.disabled) {
        return;
    }

    // 隐藏之前的错误消息
    hideError();

    // 验证输入
    if (!validateInput()) {
        return;
    }

    const text = inputText.value.trim();

    // 显示加载状态
    showLoading();

    try {
        // 调用API
        const result = await translateAPI(text);

        // 验证API返回数据
        if (!result || typeof result !== 'object') {
            throw new Error('API返回数据格式错误');
        }

        // 显示结果
        showResult(result.translation, result.keywords);

    } catch (error) {
        // 显示错误
        showError(error.message || '翻译失败，请稍后重试');
        console.error('翻译错误:', error);
    } finally {
        // 隐藏加载状态
        hideLoading();
    }
}

/**
 * 处理回车键提交
 * @param {KeyboardEvent} event - 键盘事件
 */
function handleKeyPress(event) {
    if (event.key === 'Enter' && event.ctrlKey) {
        event.preventDefault();
        handleTranslate();
    }
}

// 绑定事件监听器
translateBtn.addEventListener('click', handleTranslate);
inputText.addEventListener('keypress', handleKeyPress);

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('AI翻译助手已加载');

    // 自动聚焦到输入框
    inputText.focus();
});
