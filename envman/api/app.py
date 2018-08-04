
import json
from envman.ssm import Parameter

class Route:
    def __init__(self, method, path):
        self.method = method
        self.path = path

    def __eq__(self, other):
        return hash(self) == hash(other)
    def __ne__(self, other):
        return not(self==other)

    def __repr__(self):
        lwrmethod = self.method.lower()
        lwrpath=self.path.lower()
        return "%(lwrmethod)s(%(lwrpath)s)"%vars()
    def __hash__(self):
        h=  hash(str(self))
        return h


from api_definition import define
class App :
    apps = {}
    @classmethod
    def create(cls, name):
        app = App(name)
        return app

    @classmethod
    def get(cls):
        try :
            return cls.apps["__main__"]
        except KeyError :
            app = cls("__main__")
            define(app)
            return app

    def __init__(self, name):
        self.name = name
        self.routes = {}
        App.apps[name] = self


    def method(self, method, path):
        route = Route(method=method, path=path)
        def decorator(fn) :
            def decorated(path_params, body, query):
                return fn(path_params, body, query)
            print "adding route", str(route)
            self.routes[route] = decorated
            print self.routes
        return decorator

    def GET(self, path):
        return self.method(method="GET", path = path)


    def POST(self, path):
        return self.method(method="POST", path = path)

    def PUT(self, path):
        return self.method(method="PUT", path = path)


    def DELETE(self, path):
        return self.method(method="DELETE", path = path)


    def route(self, event):
        print "app.route received event"  , type(event)
        path = event["path"]
        method = event["httpMethod"]
        route = Route(method=method, path=path)
        method = self.routes[route]
        body = {}
        query = {}
        path_params = {}
        if "body" in event.keys():
            if event["body"] is not None and len(event["body"]):
                print "parsing body", event["body"]
                body = json.loads(event["body"])
        if "queryStringParameters" in event.keys() :
            if event["queryStringParameters"] is not None and len(event["queryStringParameters"]):
                query= event["queryStringParameters"]

        #if "pathParameters" in event.keys():
        #    if event["pathParameters"] is not None and len(event["pathParameters"]):
        #        path_params = json.loads(event["pathParameters"])
        print "Calling ", repr(route), "with \n", path_params, "\n",body, "\n", query
        return self.routes[route](path_params, body, query)



