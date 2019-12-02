from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, redirect
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = "this is secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __table_name__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

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
    title = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Post('{self.id}', '{self.title}')>"


@app.route("/", methods=["POST", "GET"])
def index():
    print(request.method)
    if request.method == "GET":
        print(User.query.all())
        # return jsonify(User.query.all())
        return jsonify("get 자체는 성공")

    elif request.method == "POST":
        print(request.json.get("username"))
        receive_username = request.json.get("username")
        receive_password = request.json.get("password")
        new_user = User(username=receive_username, password=receive_password)
        db.session.add(new_user)
        db.session.commit()

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify("store completed")

        except:
            return jsonify("there is a hot issue")

        # new_task = Todo(content = request)
        # task_content = request
        # print(request)


if __name__ == "__main__":
    app.run(debug=True)
