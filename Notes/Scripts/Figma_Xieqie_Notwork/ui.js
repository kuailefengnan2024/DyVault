// ui.js
document.getElementById('horizontal-skew').addEventListener('input', (e) => {
    const value = parseInt(e.target.value) || 0; // 确保值是整数，默认为 0
    if (value < -45 || value > 45) {
      e.target.value = Math.max(-45, Math.min(45, value)); // 限制在 -45 到 45 之间
    }
    parent.postMessage({ pluginMessage: { type: 'update-skew', horizontal: value } }, '*');
  });
  
  document.getElementById('reset').addEventListener('click', () => {
    document.getElementById('horizontal-skew').value = 0;
    parent.postMessage({ pluginMessage: { type: 'reset-skew' } }, '*');
  });
  
  document.getElementById('apply').addEventListener('click', () => {
    parent.postMessage({ pluginMessage: { type: 'apply-skew' } }, '*');
  });