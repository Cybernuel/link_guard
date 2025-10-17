import requests
import base64


def check_virustotal(url, api_key):
    if not api_key:
        return None

    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"

        response = requests.get(
            api_url,
            headers={"x-apikey": api_key},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            return {
                'malicious_count': stats.get('malicious', 0) + stats.get('suspicious', 0)
            }
        return None
    except:
        return None