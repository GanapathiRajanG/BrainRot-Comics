import json
try:
    import requests
except Exception:
    requests = None

payload = {
    'prompt': 'A time traveler who accidentally changes a minor historical event',
    'genre': 'sci-fi',
    'length': 'short'
}

if requests:
    resp = requests.post('http://127.0.0.1:5000/generate_story', json=payload)
    print('Status:', resp.status_code)
    try:
        print('Response:', json.dumps(resp.json(), indent=2))
    except Exception:
        print('Non-JSON response:', resp.text)
else:
    # Fallback to urllib if requests isn't installed
    from urllib.request import Request, urlopen
    data = json.dumps(payload).encode('utf-8')
    req = Request('http://127.0.0.1:5000/generate_story', data=data, headers={'Content-Type': 'application/json'})
    try:
        with urlopen(req, timeout=10) as res:
            body = res.read().decode('utf-8')
            print('Status:', res.status)
            try:
                print('Response:', json.dumps(json.loads(body), indent=2))
            except Exception:
                print('Non-JSON response:', body)
    except Exception as e:
        print('Request failed:', e)
