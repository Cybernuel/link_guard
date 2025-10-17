# 🛡️ LinkGuard - Simple URL Scanner chrome extension

Scans URLs to detect suspicious links using heuristics and VirusTotal.

## Quick Setup

### 1. Install API
```bash
cd api
pip install -r requirements.txt
```

### 2. (Optional) Add VirusTotal API Key
Get free key: https://www.virustotal.com/gui/my-apikey

```bash
export VIRUSTOTAL_API_KEY=your_key_here
```

### 3. Start API
```bash
python app.py
```

### 4. Load Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension/` folder

## Usage

1. Click the LinkGuard icon in Chrome
2. Enter a URL
3. Click "Scan URL"
4. See if it's safe or suspicious!

## What It Detects

- URL shorteners (bit.ly, etc.)
- Suspicious domains (.tk, .ml, etc.)
- IP addresses instead of domains
- Phishing keywords (login, verify, etc.)
- Long suspicious URLs
- VirusTotal threats (if API key set)

## Files

```
extension/
├── manifest.json    # Extension config
├── popup.html       # UI
└── popup.js         # Scan logic

api/
├── app.py          # Flask API
├── heuristics.py   # Detection rules
├── ti_lookup.py    # VirusTotal check
└── requirements.txt
```

That's it! Super simple. 🔥
