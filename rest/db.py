from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
	id =  db.Column(db.Integer, primary_key=True)
	fio = db.Column(db.String(100), nullable=False)


	def __repr__(self):
		return f"User(name = {fio})"
db.create_all()

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("fio", type=str, help='FIO', required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("fio", type=str, help='FIO')

resource_fields = {
	'id': fields.Integer,
	'fio': fields.String
}

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
