from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    get_jwt_identity, create_refresh_token
from config import AppConfig
from postgres_db import DataBase
from db import adr
import json
from colorama import init, Fore, Style

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(AppConfig)
server_session = Session(app)
jwt = JWTManager(app)
my_db = DataBase(**adr)
init(autoreset=True)


@app.before_request
def connect_database():
    my_db.connect()
    print(Style.BRIGHT + Fore.CYAN + "Connected to PostgresSQL", end='\n\n')


@app.after_request
def close_connection(resp):
    print(session)
    print(Style.BRIGHT + Fore.YELLOW + f"Connection is closed, response is {resp}", end='\n\n')
    return resp


@app.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def handle_refresh():
    info = get_jwt_identity()
    return {
        'access_token': create_access_token(identity=info),
        'refresh_token': create_refresh_token(identity=info)
    }


@app.route('/register', methods=['POST'])
def register_user():
    nick = request.json['nick']
    age = int(request.json['age'])
    email = request.json['email']
    password = request.json['password']

    user_exists = True if my_db.get_user_by_email(email) else False
    if not user_exists:
        hashed = generate_password_hash(password)
        my_db.insert_data(nick, age, email, hashed)
        return jsonify(msg='Registered successfully')
    else:
        return jsonify(msg='User with such email/nick is already registered ('), 409


@app.route('/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        data = json.loads(request.data)
        email, password = data['email'], data['password']
        user = my_db.get_user_by_email(email)
        if not user:
            return jsonify({
                'msg': 'User do not exists',
            }), 401
        if check_password_hash(user.password, password):
            res = {
                'id': str(user.id),
                'email': str(user.email)
            }
            if str(user.id) not in session.values():
                token = create_access_token(identity=res)
                refresh_token = create_refresh_token(identity=res)
                session[token] = str(user.id)
                return jsonify(access_token=token, refresh_token=refresh_token)
            return jsonify({'msg': 'Already authorized'}), 409
        return jsonify({
            'msg': 'Wrong password or email',
        }), 401


@app.route('/@me')
@jwt_required(locations='headers')
def users_info():
    user = get_jwt_identity()
    print(user)
    res = my_db.get_user_by_id(int(user['id']))
    return jsonify(res.id, res.nickname, res.age, res.email, res.avatar)


@app.route('/upload_post', methods=['POST'])
@jwt_required(locations='headers')
def upload_post():
    user = get_jwt_identity()
    data = request.json
    try:
        my_db.upload_post(int(user['id']), data['text'])
        return jsonify(msg='Post uploaded')
    except Exception:
        return jsonify(msg='Error occurred')


@app.route('/delete_post/<post_id>')
@jwt_required(locations='headers')
def delete_post(post_id):
    user = get_jwt_identity()['id']
    this_user_posts = my_db.get_user_posts(user)
    could_be_deleted = list(filter(lambda x: x[0] == int(post_id), this_user_posts))
    if could_be_deleted[0]:
        return jsonify(msg=my_db.delete_post(int(post_id)))
    return jsonify(msg='It seems you are truing to delete not existing post, or not your post')


@app.route('/get_posts')
@jwt_required(locations='headers')
def get_all():
    user = get_jwt_identity()
    print(my_db.get_user_posts(int(user['id'])))
    return jsonify(my_db.get_user_posts(int(user['id'])))


@app.route('/get_all_posts')
@jwt_required(locations='headers')
def get_all_posts():
    return jsonify(my_db.get_all_posts())


@app.route('/update_nickname', methods=['POST'])
@jwt_required(locations='headers')
def update_info():
    data = request.json
    user = get_jwt_identity()
    res = my_db.update_nick(int(user['id']), data['nickname'])
    return jsonify(msg=res)


@app.route('/update_avatar', methods=['POST'])
@jwt_required(locations='headers')
def update_avatar():
    data = request.data
    print(data)
    if len(data) < 1:
        return jsonify(msg='Error')
    user = get_jwt_identity()
    res = my_db.update_avatar(int(user['id']), data)
    return jsonify(msg=res)


@app.route('/logout')
@jwt_required(locations='headers')
def logout():
    del session[request.headers['Authorization'].split()[1]]
    res = 'User logout'
    return jsonify(msg=res)


if __name__ == '__main__':
    app.run()
