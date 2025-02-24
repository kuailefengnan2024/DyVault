document.addEventListener('DOMContentLoaded', function() {
  const suffixText = document.getElementById('suffixText');
  const targetUrl = document.getElementById('targetUrl');
  const saveBtn = document.getElementById('saveBtn');

  // 加载保存的设置
  chrome.storage.sync.get(['customSuffix', 'targetUrl'], function(data) {
    suffixText.value = data.customSuffix || '上述是我要给需求方的回复内容 帮我优化下语气 要自然真诚';
    targetUrl.value = data.targetUrl || 'https://grok.com';
  });

  // 保存设置
  saveBtn.addEventListener('click', function() {
    chrome.storage.sync.set({
      customSuffix: suffixText.value.trim(),
      targetUrl: targetUrl.value
    }, function() {
      alert('设置已保存！');
      window.close();
    });
  });
});