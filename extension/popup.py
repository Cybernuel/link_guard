document.addEventListener('DOMContentLoaded', () => {
  const urlInput = document.getElementById('url');
  const modeSelect = document.getElementById('mode');
  const scanBtn = document.getElementById('scan');
  const resultDiv = document.getElementById('result');

  // Load saved mode
  chrome.storage.local.get({ mode: 'heuristic' }, (items) => {
    modeSelect.value = items.mode || 'heuristic';
  });

  modeSelect.addEventListener('change', () => {
    const mode = modeSelect.value;
    chrome.storage.local.set({ mode });
    resultDiv.textContent = `Mode set to ${mode}.`;
  });

  scanBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    const mode = modeSelect.value;

    if (!url) {
      resultDiv.textContent = 'Enter a URL to scan.';
      return;
    }

    resultDiv.textContent = 'Scanning...';

    chrome.runtime.sendMessage({ action: 'popup_scan', url, mode }, (resp) => {
      if (!resp) {
        resultDiv.textContent = 'No response (backend may be unreachable).';
        return;
      }
      // Normalize
      let verdict = resp.verdict || (resp.result && resp.result.verdict) || 'unknown';
      let score = resp.score || (resp.result && resp.result.score) || (resp.ti && (resp.ti.stats && (resp.ti.stats.malicious || 0))) || 0;
      let reasons = resp.reasons || (resp.result && resp.result.reasons) || [];
      resultDiv.innerHTML = `<strong>Verdict:</strong> ${verdict.toUpperCase()}<br><strong>Score:</strong> ${score}<br><strong>Reasons:</strong> ${reasons.join(', ') || 'none'}`;
    });
  });
});
