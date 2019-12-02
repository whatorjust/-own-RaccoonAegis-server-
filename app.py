from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, redirect, make_response, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow

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
    posts = db.relationship("Post", backref="author", uselist=False)

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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) # User, Post 연동

    def __repr__(self):
        return f"<Post('{self.id}', '{self.title}')>"

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post

@app.route("/signup", methods=["POST", "DELETE"]) # 회원가입/탈퇴
def signup():
    if request.method == "POST": # 회원가입
        print (request.method)
        print (request.json)
        receive_username = request.json.get("mail")
        receive_password = request.json.get("pw")
        new_user = User(username=receive_username, password=receive_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify("정상적으로 회원가입이 완료되었습니다."), 200)

        except:
            return make_response(jsonify("중복된 아이디입니다."), 300)

    elif request.method == "DELETE": # 회원탈퇴
        print (request.method)
        receive_username = request.json.get("mail")
        receive_password = request.json.get("pw")
        deleteUser = User.query.filter_by(username = receive_username).first()

        try:
            db.session.delete(deleteUser)
            db.session.commit()
            return make_response(jsonify("정상적으로 회원탈퇴가 완료되었습니다."), 200)

        except:
            return make_response(jsonify("회원정보가 일치하지 않습니다."), 300)

@app.route("/signin", methods=["POST", "GET"]) # 로그인/아웃
def signin():
    if request.method == "POST": # 로그인
        print (request.method)
        receive_username = request.json.get("mail")
        receive_password = request.json.get("pw")
        login_user = User.query.filter_by(username = receive_username).first()

        if session:
            return make_response(jsonify("이미 로그인이 되어있습니다."), 300)

        if login_user and check_password_hash(login_user.password, receive_password):
            # 로그인 성공 메시지, 유저정보 반환, 토큰 발행
            session[receive_username] = True
            return make_response(jsonify("로그인이 완료되었습니다."), 200)
            
        return make_response(jsonify("회원정보가 일치하지 않습니다."), 404)

    elif request.method == "GET": # 로그아웃
        print (request.method)
        session.clear()
        return make_response(jsonify("로그아웃이 완료되었습니다."), 200)
    
@app.route("/userWord", methods=["POST", "DELETE"]) # 단어 추가/일괄 삭제
def inputWord():
    if request.method == "POST":
        print (request.method)
        if session:
            return jsonify("로그인 된 상태에서 단어 추가.")
        else:
            return jsonify("로그인이 되지 않은 상태에서 단어 추가 시도.")
        # receive_username = request.json.get("mail")
        # receive_password = request.json.get("pw")
        recieve_message = request.json.get("inputWord")
        login_user_id = User.query.filter_by(username = receive_username).first().id
        print (login_user_id)

        # asdf = Post.query.filter_by(id = login_user_id).first().content

# id1 = [바보]
# id2 = [바보, 멍청이]

# id email
# 2  hello123@email.com
# 3 slkdjflkse@email.com

# id content fkey 
# 1  바보      2
# 2  멍청이     2
# 3  천재      3



        new_post = Post(content = recieve_message, id = login_user_id)

        db.session.add(new_post)
        db.session.commit()
        asdf2 = Post.query.filter_by(id = login_user_id).first()

        return jsonify(asdf2)
        
        # username으로 id number를 조회하여 그 id number로 post 테이블을 조회한다.
        # post 테이블 안에 해당 id number를 조회하여 내용이 없으면 add, 없으면 update를 한다.
        

    elif request.method == "DELETE":
        print (request.method)

@app.route("/usemodel", methods=["POST"]) # ?
def usemodel():
    if request.method == "POST":
        print (request.method)

db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
