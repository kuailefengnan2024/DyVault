console.log('content.js 已加载 - v1.1.0');

function removeButton() {
  const existingButton = document.querySelector('#grok-enhance-btn');
  if (existingButton) {
    console.log('移除按钮');
    existingButton.remove();
  }
}

function showButton(selectedText) {
  removeButton();

  console.log('进入 showButton 函数，选中文本:', selectedText);
  const button = document.createElement('button');
  button.id = 'grok-enhance-btn';
  button.innerText = '优化文本';
  button.style.position = 'absolute';
  button.style.backgroundColor = '#4CAF50';
  button.style.color = 'white';
  button.style.border = '2px solid red'; // 醒目边框，便于调试
  button.style.padding = '5px';
  button.style.cursor = 'pointer';
  button.style.fontSize = '12px';
  button.style.zIndex = '10000';

  const range = window.getSelection().getRangeAt(0);
  const rect = range.getBoundingClientRect();
  console.log('选区坐标:', rect);
  button.style.top = `${rect.bottom + window.scrollY + 5}px`;
  button.style.left = `${rect.left + window.scrollX}px`;

  // 延迟绑定点击事件，避免事件叠加
  setTimeout(() => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      console.log('按钮被点击，选中文本:', selectedText);

      chrome.runtime.sendMessage({ action: 'get-suffix' }, (response) => {
        if (chrome.runtime.lastError) {
          console.error('发送消息失败:', chrome.runtime.lastError.message);
          return;
        }
        console.log('收到后缀文本响应:', response);
        const suffixText = response?.suffixText || "帮我优化话术，我要发给需求方 真诚自然 原意不变";
        const combinedText = `${selectedText}\n\n${suffixText}`;

        navigator.clipboard.writeText(combinedText)
        .then(() => {
          console.log('文本已成功复制到剪贴板:', combinedText);
          chrome.runtime.sendMessage({ action: 'open-url' }, () => {
            if (chrome.runtime.lastError) {
              console.error('打开新标签页消息失败:', chrome.runtime.lastError.message);
            } else {
              console.log('已发送打开新标签页请求');
            }
          });
      
          // 延迟移除按钮
          setTimeout(() => {
            removeButton();
          }, 500);  // 延迟500毫秒
        })
        .catch((err) => {
          console.error('复制到剪贴板失败:', err);
        });
      
      });
    });
    document.body.appendChild(button);
    console.log('按钮已创建并添加到页面，检查 DOM:', document.querySelector('#grok-enhance-btn'));
  }, 100); // 延迟 100ms
}

document.addEventListener('mouseup', (e) => {
  e.stopPropagation();
  console.log('mouseup 事件触发');
  const selectedText = window.getSelection().toString().trim();
  console.log('当前选中文本:', selectedText);
  if (selectedText) {
    showButton(selectedText);
  } else {
    removeButton();
  }
});

document.addEventListener('mousedown', (e) => {
  e.stopPropagation();
  setTimeout(() => {
    const selectedText = window.getSelection().toString().trim();
    if (!selectedText && e.target.id !== 'grok-enhance-btn') {
      removeButton();
    }
  }, 0);
});