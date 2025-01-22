from urllib.parse import parse_qs

HELLO_WORLD = b"Hello world!\n"




def app(environ, start_response):
    status = '200 OK'
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    print()
    if request_body_size > 0:
        print("BODY SIZE:", request_body_size)

    print("METHOD:", environ['REQUEST_METHOD'])

    if environ['REQUEST_METHOD'] == "GET":
        d = parse_qs(environ['QUERY_STRING'])
        print("QUERY PARAMS:", end=" ")
        print(d)
    elif environ['REQUEST_METHOD'] == "POST":
        request_body = environ['wsgi.input'].read(request_body_size)
        print("BODY:", f"{request_body}")
    
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]

application = app