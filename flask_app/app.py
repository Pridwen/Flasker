from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
import os

# with app.app_context():
    # db.create_all()
    # db.session.commit()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'blabla_bla'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'booksA.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    Author = db.Column(db.String(50), unique=True, nullable=False)
    Publisher = db.Column(db.String(50), nullable=False)
    book_prize = db.Column(db.Integer)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Numa bun': 'Inregistrat cumatrul'})


@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = Users.query.all()
    result = []
    for user in users:
        user_data = {'public_id': user.public_id, 'name': user.name, 'password': user.password, 'admin': user.admin}
        result.append(user_data)
    return jsonify({'users': result})


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    # print(auth)
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})
    user = Users.query.filter_by(name=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token})
    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@app.route('/book', methods=['POST'])
@token_required
def create_book(current_user):
    data = request.get_json()
    new_books = Books(name=data['name'], Author=data['Author'], Publisher=data['Publisher'],
                      book_prize=data['book_prize'], user_id=current_user.id)
    db.session.add(new_books)
    db.session.commit()
    return jsonify({'message': 'Carte noua'})


@app.route('/books', methods=['GET'])
@token_required
def get_books(current_user):
    books = Books.query.filter_by(user_id=current_user.id).all()
    output = []
    for book in books:
        book_data = {'id': book.id, 'name': book.name, 'Author': book.Author, 'Publisher': book.Publisher,
                     'book_prize': book.book_prize}
        output.append(book_data)
    return jsonify({'list_of_books': output})


@app.route('/books/<book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, book_id):
    book = Books.query.filter_by(id=book_id, user_id=current_user.id).first()
    if not book:
        return jsonify({'message': 'book does not exist'})
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})


if __name__ == '__main__':
    app.run(host="localhost", port="0698", debug=True)
