from flask import Flask, request, jsonify
from flask_cors import CORS
from heuristics import analyze_url_heuristics
from ti_lookup import check_virustotal
import os

app = Flask(__name__)
CORS(app)

VT_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')


@app.route('/api/check-url', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL required'}), 400

    # Run checks
    heuristic = analyze_url_heuristics(url)
    vt_result = check_virustotal(url, VT_API_KEY) if VT_API_KEY else None

    # Combine results
    suspicious = heuristic['suspicious']
    reasons = heuristic['reasons']
    score = heuristic['score']

    if vt_result and vt_result['malicious_count'] > 0:
        suspicious = True
        reasons.append(f"Flagged by {vt_result['malicious_count']} security vendors")
        score += vt_result['malicious_count'] * 10

    return jsonify({
        'url': url,
        'suspicious': suspicious,
        'reasons': reasons,
        'score': min(score, 100)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)