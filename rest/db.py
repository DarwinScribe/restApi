from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#класс для создания модели сущности в базе
class UserModel(db.Model):
	id =  db.Column(db.Integer, primary_key=True)
	fio = db.Column(db.String(100), nullable=False)


	def __repr__(self):
		return f"User(name = {fio})"

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("fio", type=str, help='FIO', required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("fio", type=str, help='FIO')

resource_fields = {
	'id': fields.Integer,
	'fio': fields.String
}
#класс user реализующий методы вставки, удаления, обноления и получения данных
#данные проходят через resource_fields и передаются в нужном формате в класс UserModel,
#в мотдах на обновление и вставку данных, полученная из запроса инофрмация проходит через reqparse.RequestParser()
#тем самым улучшая доступ к информации, а случае с вставкой делает обязательным ввод фио
class User(Resource):
	@marshal_with(resource_fields)
	def get(self, user_id):
		result = UserModel.query.filter_by(id=user_id).first()
		if not result:
			abort(404, message='Not find....')
		return result

	@marshal_with(resource_fields)
	def put(self, user_id):
		args = user_put_args.parse_args()
		result = UserModel.query.filter_by(id=user_id).first()
		if result:
			abort(409, message='user already exist....')
		new_user = UserModel(id=user_id, fio=args['fio'])
		db.session.add(new_user)
		db.session.commit()
		return new_user, 201

	@marshal_with(resource_fields)	
	def patch(self, user_id):
		args = user_update_args.parse_args()
		result = UserModel.query.filter_by(id=user_id).first()
		if not result:
			abort(404, message='user doesn exist....')
		if args['fio']:
			result.fio = args['fio']
		db.session.commit()
		
		return result

	@marshal_with(resource_fields)
	def delete(self, user_id):
		result = UserModel.query.filter_by(id=user_id).first()
		if not result:
			abort(404, message='user doesn exist....')
		db.session.delete(result)
		db.session.commit()
		return result, 204


api.add_resource(User, "/user/<int:user_id>")

if __name__ == "__main__":
	app.run(debug=True)

