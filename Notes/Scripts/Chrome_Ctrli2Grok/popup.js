document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.getElementById("customText");
  const saveBtn = document.getElementById("saveBtn");

  // 加载保存的自定义文本
  chrome.storage.sync.get({
    customText: "帮我优化语气 显得自然真诚 发送对象是公司的需求方"
  }, (data) => {
    try {
      textarea.value = data.customText || "";
    } catch (error) {
      console.error("加载自定义文本失败:", error);
    }
  });

  // 保存自定义文本
  saveBtn.addEventListener("click", () => {
    try {
      const customText = textarea.value.trim();
      if (customText) {
        chrome.storage.sync.set({
          customText: customText
        }, () => {
          console.log("自定义文本已保存:", customText);
          alert("设置已保存");
        });
      } else {
        alert("请输入自定义文本");
      }
    } catch (error) {
      console.error("保存自定义文本失败:", error);
      alert("保存失败，请重试");
    }
  });

  // 防止输入框或快捷键区域的事件导致崩溃
  textarea.addEventListener("input", (e) => {
    console.log("输入框内容变化:", e.target.value);
  });

  // 确保快捷键提示区域不会触发意外事件
  const shortcutDiv = document.querySelector(".shortcut");
  if (shortcutDiv) {
    shortcutDiv.addEventListener("click", (e) => {
      console.log("快捷键提示被点击");
      e.preventDefault(); // 防止默认行为
    });
  }
});