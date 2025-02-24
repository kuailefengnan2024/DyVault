document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("customText");
    const saveBtn = document.getElementById("saveBtn");
  
    // 加载保存的自定义文本
    chrome.storage.sync.get({
      customText: "帮我优化语气 显得自然真诚 发送对象是公司的需求方"
    }, (data) => {
      textarea.value = data.customText;
    });
  
    // 保存自定义文本
    saveBtn.addEventListener("click", () => {
      chrome.storage.sync.set({
        customText: textarea.value
      }, () => {
        alert("设置已保存");
      });
    });
  });