# pip install Flask-HTTPAuth
try:
    from flask import Flask
    from flask_restful import Resource,Api
    from flask_restful import reqparse
    from flask import request
    from flask_httpauth import HTTPBasicAuth
    import jwt
    import datetime
    import json
    print("All modules loaded ")
except Exception as e:
    print("Error : {} ".format(e))


app = Flask(__name__)
api = Api(app)


class Controller(Resource):
    def __init__(self):
        self.name = parser.parse_args().get("name")

    def get(self):

        data = dict(request.headers)
        print('-'*55)
        print(data)
        print('-'*55)
        agent = data.get("User-Agent")

        if "python" in agent:
            return {"Message":"You are a bot and you are not allowed to hack me "},404
        else:

            return {
                       "message" : "Hello World",
                       "name":self.name
                   }, 200

parser = reqparse.RequestParser()
api.add_resource(Controller, '/')
parser.add_argument("name", type=str, required=True, help="Query parameters is required ")


if __name__ == "__main__":
    app.run(debug=True)
