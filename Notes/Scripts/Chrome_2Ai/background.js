// 监听来自内容脚本的消息
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'openTab') {
    // 创建新标签页
    chrome.tabs.create({ url: request.url }, function(tab) {
      if (chrome.runtime.lastError) {
        // 如果创建标签页失败，返回错误信息
        sendResponse({ success: false, error: chrome.runtime.lastError.message });
      } else {
        // 标签页成功打开，返回成功响应
        sendResponse({ success: true });
      }
    });

    // 必须返回 true 以便使用异步响应
    return true;
  }
});
