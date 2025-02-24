chrome.commands.onCommand.addListener((command) => {
  if (command === "enhance-text") {
    console.log("快捷键 Ctrl+I 被触发");
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
      if (tabs.length > 0) {
        const tab = tabs[0];
        console.log("目标标签页 ID:", tab.id, "URL:", tab.url);

        // 动态注入脚本以获取选中文本
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          function: getSelectedTextDynamically
        }, (results) => {
          if (chrome.runtime.lastError) {
            console.error("动态注入脚本失败 (获取选中文本):", chrome.runtime.lastError.message || chrome.runtime.lastError);
            alert("无法获取选中文本，请确保页面允许扩展程序运行或刷新页面后重试。");
          } else if (results && results[0] && results[0].result) {
            console.log("动态获取选中文本:", results[0].result);
            processTextInBackground(results[0].result);
          } else {
            console.warn("未获取到选中文本");
          }
        });
      } else {
        console.error("未找到活动标签页");
      }
    });
  }
});

// 动态获取选中文本的函数
function getSelectedTextDynamically() {
  return window.getSelection().toString().trim();
}

// 直接在背景脚本处理文本
function processTextInBackground(text) {
  navigator.clipboard.writeText(text)
    .then(() => {
      console.log("文本已成功复制到剪贴板");
      chrome.storage.sync.get({customText: "帮我优化语气 显得自然真诚 发送对象是公司的需求方"}, (data) => {
        const fullText = `${text}\n\n${data.customText}`;
        console.log("完整文本:", fullText);
        // 尝试创建新标签页并处理可能的错误
        chrome.tabs.create({
          url: "https://grok.com"
        }, (newTab) => {
          if (chrome.runtime.lastError) {
            console.error("创建新标签页失败:", chrome.runtime.lastError.message || chrome.runtime.lastError);
            alert("无法打开 Grok 页面，请检查网站状态或稍后重试。");
          } else {
            console.log("已打开新标签页:", newTab.id);
          }
        });
      });
    })
    .catch((error) => {
      console.error("复制到剪贴板失败:", error);
      // 备用剪贴板方法
      chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          function: copyToClipboardFallback,
          args: [text]
        }, (results) => {
          if (chrome.runtime.lastError) {
            console.error("备用复制方法失败:", chrome.runtime.lastError);
          } else {
            console.log("使用备用方法复制到剪贴板成功");
          }
        });
      });
    });
}

// 备用函数：复制到剪贴板
function copyToClipboardFallback(text) {
  const tempInput = document.createElement("textarea");
  tempInput.value = text;
  document.body.appendChild(tempInput);
  tempInput.select();
  try {
    document.execCommand("copy");
    console.log("备用方法复制到剪贴板成功");
  } catch (copyError) {
    console.error("备用复制方法失败:", copyError);
  }
  document.body.removeChild(tempInput);
}