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
auth = HTTPBasicAuth()

USER_DATA = {
    "admin":"admin"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class Controller(Resource):
    def __init__(self):
        self.name = parser.parse_args().get("name")

    @auth.login_required
    def get(self):
        return {
                   "message" : "Hello World",
                   "name":self.name
               }, 200


parser = reqparse.RequestParser()
api.add_resource(Controller, '/')
parser.add_argument("name", type=str, required=True, help="Query parameters is required ")


if __name__ == "__main__":
    app.run(debug=True)
