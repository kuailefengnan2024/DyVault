console.log('background.js 已加载');

// 初始化默认值并创建菜单
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    suffixText: "帮我优化话术，我要发给需求方 真诚自然 原意不变",
    customUrl: "https://grok.com"
  }, () => {
    console.log('初始化默认值完成');
  });

  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({
      id: "enhance-text",
      title: "优化选中文本",
      contexts: ["selection"]
    }, () => {
      if (chrome.runtime.lastError) {
        console.error('创建菜单失败:', chrome.runtime.lastError.message);
      } else {
        console.log('右键菜单已创建');
      }
    });
  });
});

// 处理右键菜单点击
chrome.contextMenus.onClicked.addListener((info, tab) => {
  console.log('右键菜单点击事件触发，info:', info, 'tab:', tab);
  if (info.menuItemId === "enhance-text") {
    const selectedText = info.selectionText;
    console.log('选中文本:', selectedText);

    chrome.storage.local.get(['suffixText', 'customUrl'], (result) => {
      console.log('存储获取结果:', result);
      const suffixText = result.suffixText || "帮我优化话术，我要发给需求方 真诚自然 原意不变";
      const combinedText = `${selectedText}\n\n${suffixText}`;
      const url = result.customUrl || "https://grok.com";

      // 检查 scripting API 是否可用
      if (chrome.scripting) {
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: (text) => {
            navigator.clipboard.writeText(text)
              .then(() => console.log('文本已复制到剪贴板:', text))
              .catch(err => console.error('复制失败:', err));
          },
          args: [combinedText]
        }, () => {
          if (chrome.runtime.lastError) {
            console.error('执行脚本失败:', chrome.runtime.lastError.message);
          } else {
            console.log('脚本执行完成');
          }
        });
      } else {
        console.warn('chrome.scripting 不可用，使用备用方案');
        chrome.tabs.sendMessage(tab.id, { action: "copyText", text: combinedText }, (response) => {
          if (chrome.runtime.lastError) {
            console.error('发送消息失败:', chrome.runtime.lastError.message);
          } else {
            console.log('已通过 content.js 复制文本');
          }
        });
      }

      // 打开新标签页
      chrome.tabs.create({ url: url }, (newTab) => {
        if (chrome.runtime.lastError) {
          console.error('创建新标签页失败:', chrome.runtime.lastError.message);
        } else {
          console.log('新标签页已打开，ID:', newTab.id);
        }
      });
    });
  }
});

// 响应 Popup UI 的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('收到消息:', message);
  if (message.action === 'get-suffix') {
    chrome.storage.local.get(['suffixText'], (result) => {
      const suffix = result.suffixText || "帮我优化话术，我要发给需求方 真诚自然 原意不变";
      console.log('返回后缀文本:', suffix);
      sendResponse({ suffixText: suffix });
    });
    return true;
  } else if (message.action === 'copyText') {
    console.log('收到复制请求，文本:', message.text);
    // 这里不需要处理，交给 content.js
    sendResponse({ success: true });
  }
});