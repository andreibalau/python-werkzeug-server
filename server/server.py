from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule  # , NotFound, RequestRedirect, HTTPException
import os, json
import pprint

url_map = Map([
    Rule('/', endpoint='index')
])


class Server:

    def index(self, **kwarg):
        return {'state': True, 'message': 'First Page, default route'}

    def __call__(self, environ, start_response):
        request = Request(environ)
        res = {}
        urls = url_map.bind_to_environ(environ)
        try:
            endpoint, args = urls.match()
        except:
            endpoint, args = ('index', {})
        func = self.index
        if hasattr(self, endpoint):
            func = getattr(self, endpoint)
        args['request'] = request
        res = func(**args)
        response = Response(content_type="application/json")
        if res:
            response.headers["Cache-Control"] = "no-cache"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "-1"
            response.data = json.dumps(res)
        return response(environ, start_response)


if __name__ == '__main__':
    server = Server()
    run_simple('0.0.0.0', 8020, server)
