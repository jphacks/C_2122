import sqlite3
from collections import defaultdict

import flask
import flask_login
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import models.database as modeldb

SECRET_KEY = "secret_key"

app = flask.Flask(
        __name__,
        template_folder="static")
app.config["SECRET_KEY"] = SECRET_KEY
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, user_id):
        self.id = user_id
    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def get_abs(path):
    # 共通部分の読み込み
    f = open("static/"+path, 'r')
    read = f.read()
    f.close()
    return read


@app.route('/', methods=["POST", "GET"])
def index():
    # スタートページを表示
    # return flask.render_template("index.html", navbar=NAVBAR, headend=HEADEND)
    return flask.render_template("index.html", abs_path=get_abs)


@app.route('/css/style.css', methods=["POST", "GET"])
def css():
    return flask.render_template("css/style.css", abs_path=get_abs)


@app.route("/login.html", methods=["POST", "GET"])
def login():
    # loginページの処理
    if(flask.request.method == "POST"):
        # ユーザーチェック
        conn = sqlite3.connect('chat_test.db')
        c = conn.cursor()
        try:
            c.execute(
                "select * from user where username = '{}' and password = '{}'".format(flask.request.form["name"], flask.request.form["password"]))
        except:
            return flask.abort(401)
        user = c.fetchall()
        if user != []:
            conn.close()
            flask_login.login_user(User(user[0][0]))
            return flask.redirect("/")
        else:
            print(c.fetchall())
            return flask.abort(401)
    return flask.render_template("login.html", abs_path=get_abs)


@app.route("/logout", methods=["GET"])
@flask_login.login_required
def logout():
    # logoutの処理
    flask_login.logout_user()
    return flask.redirect("/")


@app.route("/dashboard", methods=["POST", "GET"])
def show_dashboard():
    # dashboardの表示
    pass

#ここからあああああ、チャットオオオオ処理
@app.route("/room.html")
def room():
    conn = sqlite3.connect('chat_test.db')
    c = conn.cursor()
    c.execute(
        "select reserve.id, purpose.content from reserve inner join purpose on reserve.purpose_id = purpose.id")
    room_list = c.fetchall()
    conn.close()
    return flask.render_template("room.html", tpl_room_list=room_list, abs_path=get_abs)


@app.route("/chat.html/<int:reserveid>")
def chat(reserveid):
    conn = sqlite3.connect('chat_test.db')
    c = conn.cursor()
    c.execute(
        "select chat.content from chat where chat.reserve_id = ?", (reserveid,)
        )
    chat_fetch = c.fetchall()
    chat_list = []
    for chat in chat_fetch:
        chat_list.append(
            {"content": chat[0]}
        )
    c.close()
    return flask.render_template("chat.html", chat_list=chat_list, reserve_id=reserveid, abs_path=get_abs)

@app.route("/chat.html/css/chat.css")
def chcss():
    return flask.render_template("css/chat.css", abs_path=get_abs)


@app.route("/chat.html/<int:reserveid>", methods=["POST"])
def chat_post(reserveid):
    chat_message = flask.request.form.get("input_message")
    conn = sqlite3.connect('chat_test.db')
    c = conn.cursor()
    c.execute("insert into chat values(?,101,?,101)",
    (reserveid, chat_message))
    conn.commit()
    c.close()
    return flask.redirect("/chat.html/{}".format(reserveid))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)
