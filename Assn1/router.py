import os
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
        file_path = os.path.join("static", request.uri[len("/static/"):])
        if os.path.isfile(file_path):
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
        else:
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

    if request.uri == "/":
        filename = "index.html"
    else:
        filename = request.uri.lstrip("/")+".html"
    filepath= os.path.join("templates", filename)
    if os.path.isfile(filepath):
        return Response(
            version=request.version,
            code=200,
            reason="OK",
            headers={"Content-Type": "text/html"},
            body=open(filepath, 'r').read()
        )
    else:
        return Response(
            version=request.version,
            code=404,
            reason="Not Found",
            headers={"Content-Type": "text/html"},
            body="<h1>404 Not Found</h1><p>The requested file was not found on this server.</p>"
        )