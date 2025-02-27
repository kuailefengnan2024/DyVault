console.log('content.js 已加载');

// 预定义后缀选项
const suffixOptions = {
  "optimize-tone": "上述是我要给需求方的回复内容 帮我优化下语气 要自然真诚",
  "translate": "帮我翻译上述文案为中文,如果上述文案是中文则翻译为英文",
  "summarize": "帮我解释重点概念 精确提炼上述文案的内容,必要可以打形象的比喻 不要说废话",
  "refine-work": "上述文案是工作文档中的内容,帮我优化话术",
  "none": ""
};

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

    chrome.storage.sync.get({
      selectedSuffix: 'optimize-tone', // 默认选项为 "优化语气"
      targetUrl: 'https://grok.com'
    }, function(data) {
      const suffixKey = data.selectedSuffix || 'optimize-tone';
      const suffix = suffixOptions[suffixKey];
      console.log('当前选择的选项:', suffixKey, '后缀:', suffix);

      const appendedText = selectedText + (suffix ? '\n\n' + suffix : '');
      console.log('准备复制到剪贴板的文本:', appendedText);

      if (!appendedText.trim()) {
        console.error('appendedText 为空，无法复制');
        return;
      }

      // 优先使用 navigator.clipboard API
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(appendedText)
          .then(() => {
            console.log('文本已通过 navigator.clipboard 复制到剪贴板:', appendedText);
            window.open(data.targetUrl, '_blank');
            removeButton();
          })
          .catch(err => {
            console.error('navigator.clipboard 复制失败:', err);
            fallbackCopy(appendedText, data.targetUrl); // 回退方案
          });
      } else {
        // 回退到 document.execCommand
        fallbackCopy(appendedText, data.targetUrl);
      }
    });
  });

  document.body.appendChild(button);
}

// 回退复制方案
function fallbackCopy(text, targetUrl) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
  try {
    document.execCommand('copy');
    console.log('文本已通过 execCommand 复制到剪贴板:', text);
    window.open(targetUrl, '_blank');
    removeButton();
  } catch (err) {
    console.error('execCommand 复制失败:', err);
  }
  document.body.removeChild(textArea);
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