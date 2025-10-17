# tests/test_heuristics.py
from heuristics import score_url

def test_ip_host():
    r = score_url('http://127.0.0.1/malware.exe')
    assert 'ip-host' in r['reasons'] or r['score'] >= 30

def test_shortener():
    r = score_url('http://bit.ly/abcdefg')
    assert 'shortener' in r['reasons'] or r['score'] >= 20

def test_benign():
    r = score_url('https://example.com/about')
    assert r['verdict'] == 'allow' or r['score'] < 25
