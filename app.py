from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, redirect, make_response, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow
import machine_learning
from machine_learning import deep_model_user

# print(flask.__version__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = "this is secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __table_name__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __init__(self, username, password, **kwargs):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f"<User('{self.id}', '{self.username}')>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    __table_name__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # User, Post 연동

    def __repr__(self):
        return f"<Post('{self.id}')>"


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post

# # @app.route("/", methods=["GET"])
# # def testing():
#     return jsonify(test2.asdf)

@app.route("/signup", methods=["POST", "DELETE"])  # 회원가입/탈퇴
def signup():
    if request.method == "POST":  # 회원가입
        print(request.method)
        print(request.json)
        receive_username = request.json.get("mail")
        receive_password = request.json.get("pw")
        new_user = User(username=receive_username, password=receive_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify("정상적으로 회원가입이 완료되었습니다."), 200)

        except:
            return make_response(jsonify("중복된 아이디입니다."), 300)

    elif request.method == "DELETE":  # 회원탈퇴
        print(request.method)
        receive_username = request.json.get("mail")
        receive_password = request.json.get("pw")
        deleteUser = User.query.filter_by(username=receive_username).first()

        try:
            db.session.delete(deleteUser)
            db.session.commit()
            return make_response(jsonify("정상적으로 회원탈퇴가 완료되었습니다."), 200)

        except:
            return make_response(jsonify("회원정보가 일치하지 않습니다."), 300)


@app.route("/signin", methods=["POST", "GET"])  # 로그인/아웃
def signin():
    if request.method == "POST":  # 로그인
        print(request.method)
        receive_username = request.json.get("mail")
        receive_password = request.json.get("pw")
        login_user = User.query.filter_by(username=receive_username).first()

        # if session:
        #     return make_response(jsonify("이미 로그인이 되어있습니다."), 300)

        if login_user and check_password_hash(login_user.password, receive_password):
            # 로그인 성공 메시지, 유저정보 반환, 토큰 발행
            session["username"] = receive_username
            print(session["username"])
            # return_arr = []
            # login_user_word = (
            #     User.query.filter_by(username=session["username"]).first().posts
            # )
            # for user in login_user_word:
            #     return_arr.append(Post.query.filter_by(id=user.id).first().content)
            # return make_response(jsonify({"userWord": return_arr}), 200)
            return make_response(jsonify("로그인이 완료되었습니다."), 200)

        return make_response(jsonify("회원정보가 일치하지 않습니다."), 404)

    elif request.method == "GET":  # 로그아웃
        print(request.method)
        session.clear()
        return make_response(jsonify("로그아웃이 완료되었습니다."), 200)


@app.route("/inputWord", methods=["GET", "POST", "DELETE"])  # 단어 추가/일괄 삭제
def inputWord():
    if session:
        if request.method == "GET":
            return_arr = []
            login_user_word = (
                User.query.filter_by(username=session["username"]).first().posts
            )
            for user in login_user_word:
                return_arr.append(Post.query.filter_by(id=user.id).first().content)
            return jsonify({"userWord": return_arr})


        if request.method == "POST":
            recieve_message = request.json.get("inputWord")
            login_user_id = (
                User.query.filter_by(username=session["username"]).first().id
            )
            new_post = Post(content=recieve_message, user_id=login_user_id)
            db.session.add(new_post)
            db.session.commit()
            return_arr = []
            login_user_word = (
                User.query.filter_by(username=session["username"]).first().posts
            )
            for user in login_user_word:
                return_arr.append(Post.query.filter_by(id=user.id).first().content)
            return jsonify({"userWord": return_arr})

        elif request.method == "DELETE":
            login_user_id = (
                User.query.filter_by(username=session["username"]).first().id
            )
            Post.query.filter_by(user_id=login_user_id).delete()
            db.session.commit()
            return_arr = []
            login_user_word = (
                User.query.filter_by(username=session["username"]).first().posts
            )
            # print("여기야", login_user_word)
            for user in login_user_word:
                return_arr.append(Post.query.filter_by(id=user.id).first().content)
            return jsonify({"userWord": return_arr})
    else:
        return make_response(jsonify("세션이 존재하지 않습니다."), 404)


@app.route("/usemodel", methods=["POST"])  # ?
def usemodel():
    if request.method == "POST":
        request_text = request.json.get("text")
        return make_response({"prob" : deep_model_user.deep_learn(request_text)}, 200)


db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
