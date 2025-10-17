// LinkGuard Content Script - Scans links on page
console.log('LinkGuard: Content script loaded');

const API_URL = 'http://localhost:5000/api/check-url';
const scannedLinks = new Set();
let suspiciousCount = 0;
let isScanning = false;

// Initialize on load
chrome.storage.local.get(['enabled'], (result) => {
  if (result.enabled !== false) {
    setTimeout(scanPage, 1000);
  }
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'scan') {
    scanPage();
    sendResponse({ success: true });
  } else if (request.action === 'getStats') {
    sendResponse({
      total: scannedLinks.size,
      suspicious: suspiciousCount
    });
  }
  return true;
});

async function scanPage() {
  if (isScanning) return;
  isScanning = true;

  console.log('LinkGuard: Starting page scan...');
  const links = document.querySelectorAll('a[href]');
  let newSuspicious = 0;

  for (const link of links) {
    const url = link.href;

    if (scannedLinks.has(url) || !url.startsWith('http')) {
      continue;
    }

    scannedLinks.add(url);

    try {
      const result = await checkUrl(url);

      if (result.suspicious) {
        markLinkAsSuspicious(link, result);
        suspiciousCount++;
        newSuspicious++;
      }
    } catch (error) {
      console.error('LinkGuard: Error checking URL:', error);
    }
  }

  chrome.runtime.sendMessage({
    action: 'updateBadge',
    count: suspiciousCount
  });

  console.log(`LinkGuard: Scan complete. Found ${suspiciousCount} suspicious links`);
  isScanning = false;
}

async function checkUrl(url) {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    if (!response.ok) throw new Error('API request failed');
    return await response.json();
  } catch (error) {
    console.error('LinkGuard: API error:', error);
    return { suspicious: false, reasons: [], score: 0 };
  }
}

function markLinkAsSuspicious(link, result) {
  link.style.cssText = `
    border: 2px solid #ff4444 !important;
    background-color: rgba(255, 68, 68, 0.1) !important;
    padding: 2px 4px !important;
    border-radius: 3px !important;
    position: relative !important;
  `;

  const warningIcon = document.createElement('span');
  warningIcon.innerHTML = '⚠️';
  warningIcon.style.cssText = 'margin-left: 4px; font-size: 14px;';
  link.appendChild(warningIcon);

  const tooltip = document.createElement('div');
  tooltip.className = 'linkguard-tooltip';
  tooltip.innerHTML = `
    <strong>⚠️ Suspicious Link Detected</strong><br>
    ${result.reasons.map(r => `• ${r}`).join('<br>')}
    <br><br><em>Risk Score: ${result.score}/100</em>
  `;
  tooltip.style.cssText = `
    display: none; position: absolute; background: #fff;
    border: 2px solid #ff4444; border-radius: 6px;
    padding: 10px; z-index: 999999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    max-width: 300px; font-size: 12px;
    color: #333; line-height: 1.4;
  `;

  link.appendChild(tooltip);

  link.addEventListener('mouseenter', () => tooltip.style.display = 'block');
  link.addEventListener('mouseleave', () => tooltip.style.display = 'none');

  link.addEventListener('click', (e) => {
    e.preventDefault();
    const msg = `⚠️ LinkGuard Warning!\n\nThis link appears suspicious:\n${result.reasons.join('\n')}\n\nRisk Score: ${result.score}/100\n\nDo you want to proceed anyway?`;
    if (confirm(msg)) {
      window.location.href = link.href;
    }
  });
}

const observer = new MutationObserver(() => {
  if (!isScanning) scanPage();
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});