from request import Request
from response import Response

def parse_request(data):
    
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    
    parts= text.split("\r\n\r\n", 1)
    head= parts[0]
    headers = {}
    lines = head.split("\r\n")
    if len(lines) < 1:
        return None
    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
    body=parts[1] if len(parts)>1 else ""

    line = head.split("\r\n")
    request_line = line[0].split(" ")
    if len(request_line) != 3:
        return None
    method = request_line[0]
    uri = request_line[1]
    version = request_line[2]

    return Request(method, uri, version, body, headers)

def encode_response(response):
    if not isinstance(response, Response):
        return None
    
    status_line = f"{response.version} {response.code} {response.reason}\r\n"
    headers = ""
    for key, value in response.headers.items():
        headers += f"{key}: {value}\r\n"

    headers += "Connection: close\r\n"

    return (status_line + headers + "\r\n" + response.body).encode("utf-8")