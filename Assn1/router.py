import datetime
from response import Response

# MiddlewareFactory composes the middleware chain and returns a handler
def MiddlewareFactory(router):
    def handler(request):
        return logging_middleware(request, lambda req: static_file_middleware(req, router))
    return handler

def logging_middleware(request, next_middleware):
    print(f"Received request: {request.method} {request.uri}")
    if next_middleware:
        response = next_middleware(request)
    else:
        response = None
    
    if response:
        print(f"Responded to {request.uri} with {response.code} {response.reason}")
    return response

def static_file_middleware(request, next_middleware):
    # Serve .js and .css files from the static folder if URI contains a period
    if "." in request.uri and request.uri.startswith("/static/"):
        file_path = "static/" + request.uri[len("/static/"):]
        try:
            # Set correct Content-Type
            if file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'application/octet-stream'
            with open(file_path, 'r') as f:
                content = f.read()
            return Response(
                version=request.version,
                code=200,
                reason="OK",
                headers={"Content-Type": content_type},
                body=content
            )
        except FileNotFoundError:
            return Response(
                version=request.version,
                code=404,
                reason='Not Found',
                headers={"Content-Type": "text/html"},
                body='<h1>404 Not Found</h1><p>The requested file was not found on this server.</p>'
            )
    if next_middleware:
        return next_middleware(request)
    return None

def router(request):
    # Handle the request and return a response
    server_id = "My basic HTTP Server"
    date_str = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    connection = "close"
    cache_control = "max-age=5"

    if request.uri == "/":
        filename = "index.html"
    elif request.uri == "/info":
        return Response(
            version=request.version,
            code=301,
            reason="OK",
            headers={
                "Server": server_id,
                "Date": date_str,
                "Connection": connection,
                "Cache-Control": cache_control,
                "Location": "/about"
                },
            body="<h1>301 Moved Permanently</h1><p>Redirecting to <a href='/about'>/about</a></p>"
        )
    else:
        filename = request.uri.lstrip("/")+".html"
    filepath = "templates/" + filename
    try:
        with open(filepath, 'r') as f:
            text = f.read()
        return Response(
            version=request.version,
            code=200,
            reason="OK",
            headers={"Server": server_id,
                "Date": date_str,
                "Connection": connection,
                "Cache-Control": cache_control,
                "Content-Type": "text/html",
                "Content-Length": str(len(text.encode("utf-8"))},
            body=text
        )
    except FileNotFoundError:
        return Response(
            version=request.version,
            code=404,
            reason="Not Found",
            headers={"Server": server_id,
                "Date": date_str,
                "Connection": connection,
                "Cache-Control": cache_control,
                "Content-Type": "text/html"},
            body="<h1>404 Not Found</h1><p>The requested file was not found on this server.</p>"
        )