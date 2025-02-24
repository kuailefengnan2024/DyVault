console.log('content.js 已加载');

// 移除按钮
function removeButton() {
  const existingButton = document.querySelector('#grok-enhance-btn');
  if (existingButton) {
    existingButton.remove();
  }
}

// 显示按钮
function showButton(selectedText) {
  removeButton();

  const button = document.createElement('button');
  button.id = 'grok-enhance-btn';
  button.innerText = '>Ai';
  button.style.position = 'absolute';
  button.style.backgroundColor = '#4CAF50';
  button.style.color = 'white';
  button.style.border = 'none';
  button.style.padding = '2px 5px';
  button.style.cursor = 'pointer';
  button.style.fontSize = '8px';
  button.style.zIndex = '100000';
  button.style.borderRadius = '5px';
  button.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.3)';

  const range = window.getSelection().getRangeAt(0);
  const rect = range.getBoundingClientRect();
  button.style.top = `${rect.bottom + window.scrollY + 5}px`;
  button.style.left = `${rect.left + window.scrollX}px`;

  button.addEventListener('mouseenter', function() {
    console.log('鼠标进入按钮区域，选中文本:', selectedText);

    // 获取用户保存的设置
    chrome.storage.sync.get({
      customSuffix: '上述是我要给需求方的回复内容 帮我优化下语气 要自然真诚',
      targetUrl: 'https://grok.com'
    }, function(data) {
      const appendedText = selectedText + '\n\n' + data.customSuffix;

      const textArea = document.createElement('textarea');
      textArea.value = appendedText;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      console.log('文本已成功复制到剪贴板:', appendedText);

      window.open(data.targetUrl, '_blank');
      removeButton();
    });
  });

  document.body.appendChild(button);
}

document.addEventListener('mouseup', function(e) {
  const selectedText = window.getSelection().toString().trim();
  if (selectedText) {
    showButton(selectedText);
  } else {
    removeButton();
  }
});

document.addEventListener('mousedown', function(e) {
  if (e.target.id !== 'grok-enhance-btn') {
    removeButton();
  }
});