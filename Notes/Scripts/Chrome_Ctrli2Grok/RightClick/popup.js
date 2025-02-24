console.log('popup.js 已加载');

document.addEventListener('DOMContentLoaded', () => {
  const urlSelect = document.getElementById('url-select');
  const suffixSelect = document.getElementById('suffix-select');

  chrome.storage.local.get(['customUrl', 'suffixText'], (result) => {
    if (result.customUrl) {
      urlSelect.value = result.customUrl;
    }
    if (result.suffixText) {
      suffixSelect.value = result.suffixText;
    }
  });

  urlSelect.addEventListener('change', () => {
    const selectedUrl = urlSelect.value;
    chrome.storage.local.set({ customUrl: selectedUrl }, () => {
      console.log('目标网址已保存:', selectedUrl);
    });
  });

  suffixSelect.addEventListener('change', () => {
    const selectedSuffix = suffixSelect.value;
    chrome.storage.local.set({ suffixText: selectedSuffix }, () => {
      console.log('后缀文本已保存:', selectedSuffix);
    });
  });
});