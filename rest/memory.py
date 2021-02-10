from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("fio", type=str, help='FIO', required=True)

users = {}

#методы для проверки наличия или отсутвия пользователя
def abort_if_user_doesnt_exist(user_id):
		if user_id not in users:
			abort(404, message='user doesnt exist')

def abort_if_user_exists(user_id):
	if user_id in users:
		abort(409, message='user already exists')

#класс user с реализацией основных операций
class User(Resource):

	def get(self, user_id):
		abort_if_user_doesnt_exist(user_id)
		return users[user_id]

	def put(self, user_id):
		abort_if_user_exists(user_id)
		args = user_put_args.parse_args()
		users[user_id] = args
		return users[user_id], 201

	def patch(self, user_id):
		abort_if_user_doesnt_exist(user_id)
		args = user_put_args.parse_args()
		users[user_id] = args
		return users[user_id], 201

	def delete(self, user_id):
		abort_if_user_doesnt_exist(user_id)
		del users[user_id]
		return '', 204

api.add_resource(User, "/user/<int:user_id>")

if __name__ == "__main__":
	app.run(debug=True)
