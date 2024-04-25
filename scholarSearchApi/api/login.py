from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.login import Login

login_bp = Blueprint("login", __name__)
login_api = Api(login_bp)


class LoginAPI(Resource):
    def get(self):
        id = request.args.get("id")
        login = db.session.query(Login).get(id)
        if login:
            return login.to_dict()
        return {"message": "not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        parser.add_argument("password", required=True, type=str)
        args = parser.parse_args()
        login = Login(args["username"], args["password"])

        try:
            db.session.add(login)
            db.session.commit()
            return login.to_dict(), 201
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)
        args = parser.parse_args()

        try:
            login = db.session.query(Login).get(args["id"])
            if login:
                if args["username"] is not None:
                    login.username = args["username"]
                if args["password"] is not None:
                    login.password = args["password"]
                db.session.commit()
                return login.to_dict(), 200
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            login = db.session.query(Login).get(args["id"])
            if login:
                db.session.delete(login)
                db.session.commit()
                return login.to_dict()
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500


class LoginListAPI(Resource):
    def get(self):
        logins = db.session.query(Login).all()
        return [login.to_dict() for login in logins]


login_api.add_resource(LoginAPI, "/login")
login_api.add_resource(LoginListAPI, "/loginList")
