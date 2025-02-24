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

  // 创建按钮
  const button = document.createElement('button');
  button.id = 'grok-enhance-btn';
  button.innerText = '>Ai';  // 修改文案为 "问GPT"
  button.style.position = 'absolute';
  button.style.backgroundColor = '#4CAF50';
  button.style.color = 'white';
  button.style.border = 'none';
  button.style.padding = '2px 5px';  // 缩小按钮的大小
  button.style.cursor = 'pointer';
  button.style.fontSize = '8px';  // 更小的字体大小
  button.style.zIndex = '100000';  // 确保按钮位于最上层
  button.style.borderRadius = '5px';  // 添加圆角效果
  button.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.3)';  // 给按钮添加阴影，使其更突出

  // 定位按钮
  const range = window.getSelection().getRangeAt(0);
  const rect = range.getBoundingClientRect();
  button.style.top = `${rect.bottom + window.scrollY + 5}px`;
  button.style.left = `${rect.left + window.scrollX}px`;

  // 鼠标进入按钮区域时触发操作
  button.addEventListener('mouseenter', function() {
    console.log('鼠标进入按钮区域，选中文本:', selectedText);

    // 构造新的文本
    const appendedText = selectedText + '\n\n' + '上述是我要给需求方的回复内容 帮我优化下语气 要自然真诚';

    // 执行剪贴板操作，将新文案复制到剪贴板
    const textArea = document.createElement('textarea');
    textArea.value = appendedText;  // 选中文本 + 新文案
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');  // 使用 execCommand 进行同步复制
    document.body.removeChild(textArea);
    console.log('文本已成功复制到剪贴板:', appendedText);

    // 打开新标签页
    window.open('https://grok.com', '_blank');

    // 移除按钮
    removeButton();
  });

  // 将按钮添加到页面
  document.body.appendChild(button);
}

// 监听鼠标松开事件
document.addEventListener('mouseup', function(e) {
  const selectedText = window.getSelection().toString().trim();
  if (selectedText) {
    showButton(selectedText);
  } else {
    removeButton();
  }
});

// 监听鼠标按下事件，防止按钮被其他元素覆盖时关闭
document.addEventListener('mousedown', function(e) {
  // 只有点击不是按钮时才移除按钮
  if (e.target.id !== 'grok-enhance-btn') {
    removeButton();
  }
});
