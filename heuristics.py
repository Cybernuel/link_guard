import re
from urllib.parse import urlparse

URL_SHORTENERS = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'cutt.ly', 'is.gd', 'rb.gy']
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.click']
PHISHING_KEYWORDS = ['login', 'verify', 'account', 'secure', 'update', 'banking', 'suspended']


def analyze_url_heuristics(url):
    reasons = []
    score = 0

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Check URL shortener
        if any(s in domain for s in URL_SHORTENERS):
            reasons.append("URL shortener detected")
            score += 25

        # Check suspicious TLD
        if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
            reasons.append("Suspicious domain extension")
            score += 20

        # Check for IP address
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}', domain.split(':')[0]):
            reasons.append("Uses IP address instead of domain")
            score += 30

        # Check phishing keywords
        if any(kw in url.lower() for kw in PHISHING_KEYWORDS):
            reasons.append("Contains phishing-related keywords")
            score += 20

        # Check URL length
        if len(url) > 200:
            reasons.append("Unusually long URL")
            score += 10

        return {
            'suspicious': score > 30,
            'reasons': reasons,
            'score': score
        }
    except:
        return {'suspicious': False, 'reasons': [], 'score': 0}