from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, redirect
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
    completed = db.Column(db.Integer, default=0)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)

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
    # title = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text)
    # date_posted = db.Column(db.DateTime, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) # User, Post 연동

    def __repr__(self):
        return f"<Post('{self.id}', '{self.title}')>"

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post


@app.route("/", methods=["POST", "GET"]) # 테스트용 index
def index():
    # print(request.method)
    if request.method == "GET":
        user_schema = UserSchema() # marshmallow를 쓸 수 있는 User 테이블
        users = User.query.all()
        arr = []
        for user in users:
            arr.append(user_schema.dump(user))
        output = user_schema.dump(User.query.all())
        # print(output)
        # output = session.query(User).filter_by(User.id = 1)
        return jsonify(arr)
        # return jsonify("get 자체는 성공")

    elif request.method == "POST":
        print(request.json.get("username"))
        receive_username = request.json.get("username")
        receive_password = request.json.get("password")
        new_user = User(username=receive_username, password=receive_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify("store completed")

        except:
            return jsonify("there is a hot issue")

        # new_task = Todo(content = request)
        # task_content = request
        # print(request)

@app.route("/signup", methods=["POST", "DELETE"]) # 회원가입/탈퇴
def signup():
    if request.method == "POST":
        print (request.method)
        receive_username = request.json.get("username")
        receive_password = request.json.get("password")
        #users = User.query.all()
        #for user in users:
        #    if receive_username == user.username:
        #        return jsonify("중복된 ID입니다.")
        new_user = User(username=receive_username, password=receive_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify("store completed")

        except:
            return jsonify("중복된 아이디다!")

    elif request.method == "DELETE":
        print (request.method)
        receive_username = request.json.get("username")
        receive_password = request.json.get("password")
        deleteUser = User.query.filter_by(username = receive_username).first()
        print (1234, deleteUser)

        #for user in users:
        #    if receive_username == user.username and check_password_hash(user.password, receive_password):
        try:
            db.session.delete(deleteUser)
            db.session.commit()
            return jsonify("delete completed")
        #        return jsonify("유저 정보 삭제 완료!")
        except:
            return jsonify("정보가 일치하지 않습니다!")

@app.route("/signin", methods=["POST", "GET"]) # 로그인/아웃
def signin():
    if request.method == "POST":
        print (request.method)
        receive_username = request.json.get("username")
        receive_password = request.json.get("password")
        
    elif request.method == "GET":
        print (request.method)
    
@app.route("/inputWord", methods=["POST", "DELETE"]) # 단어 추가/일괄 삭제
def inputWord():
    if request.method == "POST":
        print (request.method)
    elif request.method == "DELETE":
        print (request.method)

@app.route("/usemodel", methods=["POST"]) # ?
def usemodel():
    if request.method == "POST":
        print (request.method)

db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
