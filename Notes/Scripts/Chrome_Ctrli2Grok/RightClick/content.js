console.log('content.js 已加载 - v1.0.9');

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'copyText') {
    console.log('content.js 收到复制请求，文本:', message.text);
    navigator.clipboard.writeText(message.text)
      .then(() => {
        console.log('content.js 成功复制文本:', message.text);
        sendResponse({ success: true });
      })
      .catch((err) => {
        console.error('content.js 复制失败:', err);
        sendResponse({ success: false, error: err.message });
      });
    return true; // 异步响应
  }
});