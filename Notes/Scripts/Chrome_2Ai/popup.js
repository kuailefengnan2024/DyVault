document.addEventListener('DOMContentLoaded', function() {
  const suffixSelect = document.getElementById('suffixSelect');
  const targetUrl = document.getElementById('targetUrl');
  const saveBtn = document.getElementById('saveBtn');

  // 加载保存的设置
  chrome.storage.sync.get(['selectedSuffix', 'targetUrl'], function(data) {
    suffixSelect.value = data.selectedSuffix || 'optimize-tone'; // 默认 "优化语气"
    targetUrl.value = data.targetUrl || 'https://grok.com';
  });

  // 保存设置
  saveBtn.addEventListener('click', function() {
    chrome.storage.sync.set({
      selectedSuffix: suffixSelect.value,
      targetUrl: targetUrl.value
    }, function() {
      alert('设置已保存！');
      window.close();
    });
  });
});