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
app.config['SECRET_KEY'] = 'mykey'


USER_DATA = {
    "admin":"admin"
}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class Login(Resource):

    @auth.login_required
    def get(self):
        token = jwt.encode({
            'user':request.authorization.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        }, app.config['SECRET_KEY'])

        return json.dumps({
            'token':token.decode('UTF-8')

        }, indent=3)

from functools import wraps
def verify_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token', None)
        if token is None:
            return {"Message":"Your are missing Token"}
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return {"Message":"Token is Missing or invalid"}
    return decorator


class Controller(Resource):
    def __init__(self):
        self.name = parser.parse_args().get("name")

    @verify_token
    def get(self):
        data = dict(request.headers)
        agent = data.get("User-Agent")

        if "python" in agent:
            return {"Message":"You are a bot and you are not allowed to hack me "},404
        else:
            return {
                       "message" : "Hello World",
                       "name":self.name
                   }, 200


parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=False, help="Query parameters is required ")
api.add_resource(Login, '/login')
api.add_resource(Controller, '/')


if __name__ == "__main__":
    app.run(debug=True)
