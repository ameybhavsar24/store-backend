from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    age = db.Column(db.Integer)

    def __init__(self, username, password, first_name, last_name, age):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    quantity = db.Column(db.Integer)
    priceType = db.Column(db.Enum("weight", "number", name="priceType"))
    price = db.Column(db.Integer)

    def __init__(self, name, quantity, priceType, price):
        self.name = name
        self.quantity = quantity
        self.priceType = priceType
        self.price = price

# Schemas

class UserSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'age')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'quantity', 'priceType', 'price')
item_schema  = ItemSchema()
items_schema = ItemSchema(many=True)

# Routes

class UserManager(Resource):
    @staticmethod
    def get():
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            users = User.query.all()
            return jsonify(users_schema.dump(users))
        user = User.query.get(id)
        return jsonify(user_schema.dump(user))

    @staticmethod
    def post():
        username = request.json['username']
        password = request.json['password']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        age = request.json['age']

        user = User(username, password, first_name, last_name, age)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'Message': f'User {first_name} {last_name} inserted.'
        })

    @staticmethod
    def put():
        try: id = request.args['id']
        except Exception as _: id = None
        if not id:
            return jsonify({ 'Message': 'Must provide the user ID' })
        user = User.query.get(id)

        username = request.json['username']
        password = request.json['password']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        age = request.json['age']

        user.username = username 
        user.password = password 
        user.first_name = first_name 
        user.last_name = last_name
        user.age = age 

        db.session.commit()
        return jsonify({
            'Message': f'User {first_name} {last_name} altered.'
        })

    @staticmethod
    def delete():
        try: id = request.args['id']
        except Exception as _: id = None
        if not id:
            return jsonify({ 'Message': 'Must provide the user ID' })
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {str(id)} deleted.'
        })


class ItemManager(Resource):
    @staticmethod
    def get():
        try: id = request.args['id']
        except Exception as _: id = None
        if not id:
            items = Item.query.all()
            return jsonify(items_schema.dump(items))
        item = Item.query.get(id)
        return jsonify(item_schema.dump(item))
    @staticmethod
    def post():
        name = request.json['name']
        quantity = request.json['quantity']
        priceType = request.json['priceType']
        price = request.json['price']

        item = Item(name, quantity, priceType, price)
        db.session.add(item)
        db.session.commit()
        return jsonify({
            'Message': f'Item {name} inserted.'
        })

api.add_resource(UserManager, '/api/users')
api.add_resource(ItemManager, '/api/items')

if __name__ == '__main__':
    app.run(debug=True,port=5000)
