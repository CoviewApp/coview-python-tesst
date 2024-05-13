from flask import request, jsonify
from flask_restful import Resource, Api
from app import app, db
from app.models import User

api = Api(app)

class UserListAPI(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([{'username': u.username, 'email': u.email} for u in users])

    def post(self):
        username = request.json.get('username')
        email = request.json.get('email')
        if username and email:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            return {'status': 'success', 'user': str(user)}, 201
        else:
            return {'status': 'error', 'message': 'Missing username or email'}, 400

class UserAPI(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return {'username': user.username, 'email': user.email}

    def put(self, id):
        user = User.query.get_or_404(id)
        user.username = request.json.get('username', user.username)
        user.email = request.json.get('email', user.email)
        db.session.commit()
        return {'status': 'success', 'user': str(user)}

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'status': 'success', 'message': 'User deleted'}

api.add_resource(UserListAPI, '/users')
api.add_resource(UserAPI, '/users/<int:id>')
