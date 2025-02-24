console.log('background.js 已加载');

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    suffixText: "帮我优化话术，我要发给需求方 真诚自然 原意不变",
    customUrl: "https://grok.com"
  }, () => {
    console.log('初始化默认值完成');
  });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('收到消息:', message);
  if (message.action === 'open-url') {
    chrome.storage.local.get(['customUrl'], (result) => {
      const url = result.customUrl || 'https://grok.com';
      console.log('准备打开网址:', url);
      chrome.tabs.create({ url: url }, (newTab) => {
        if (chrome.runtime.lastError) {
          console.error('创建新标签页失败:', chrome.runtime.lastError.message);
        } else {
          console.log('新标签页已打开，ID:', newTab.id);
        }
      });
    });
  } else if (message.action === 'get-suffix') {
    chrome.storage.local.get(['suffixText'], (result) => {
      const suffix = result.suffixText || "帮我优化话术，我要发给需求方 真诚自然 原意不变";
      console.log('返回后缀文本:', suffix);
      sendResponse({ suffixText: suffix });
    });
    return true;
  }
});
