from envman.ssm import Parameter




def define(app):
    class Api :

        @staticmethod
        @app.POST(path="/parameter")
        def post_parameter(path_params, body, query):
            return Parameter.put_parameter(
                env= body["env"],
                uri=body.get("uri",""),
                name = body.get("name",""),
                value = body.get("value","-")
            )

        @staticmethod
        @app.GET(path="/parameter")
        def get_parameter(path_params, body, query):
            return Parameter.get_parameter(
                env= query["env"],
                uri=query.get("uri",""),
                name = query.get("name","")
            )

        @staticmethod
        @app.GET(path="/parameters")
        def get_parameters(path_params, body, query):
            return Parameter.get_parameters(
                env= query["env"],
                uri=query.get("uri","")
            )

    return Api
