// background.js（无需修改）
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'openTab') {
    chrome.tabs.create({ url: request.url }, function(tab) {
      if (chrome.runtime.lastError) {
        sendResponse({ success: false, error: chrome.runtime.lastError.message });
      } else {
        sendResponse({ success: true });
      }
    });
    return true;
  }
});