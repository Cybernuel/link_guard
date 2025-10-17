// LinkGuard Background Script
console.log('LinkGuard: Background script loaded');

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'updateBadge') {
    updateBadge(sender.tab.id, request.count);
  }
});

function updateBadge(tabId, count) {
  if (count > 0) {
    chrome.action.setBadgeText({
      text: count.toString(),
      tabId: tabId
    });
    chrome.action.setBadgeBackgroundColor({
      color: '#ff4444',
      tabId: tabId
    });
  } else {
    chrome.action.setBadgeText({
      text: '',
      tabId: tabId
    });
  }
}

// Clear badge when tab is updated
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'loading') {
    chrome.action.setBadgeText({
      text: '',
      tabId: tabId
    });
  }
});