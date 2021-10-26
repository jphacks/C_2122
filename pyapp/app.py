print("hello, world")

import flask
import flask_login
from collections import defaultdict
from flask import *
import sqlite3

SECRET_KEY = "secret_key"

app = flask.Flask(
        __name__,
        template_folder="static")

app.secret_key = SECRET_KEY
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    # テストユーザ用のクラス
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

users = {
    # テストユーザ
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password")
}

# ユーザチェック用の辞書
nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id


@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))


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
        if(flask.request.form["name"] in user_check and flask.request.form["password"] == user_check[flask.request.form["name"]]["password"]):
            # ユーザーが存在した場合はログイン
            flask_login.login_user(users.get(user_check[flask.request.form["name"]]["id"]))
            flask.flash("ログインしました", "login_success")
            return flask.redirect("/") # ログイン後はトップページへ遷移 → ダッシュボードページ作成後はそちらへ変更
        else:
            return flask.abort(401)

    return flask.render_template("login.html", abs_path=get_abs)

@app.route("/logout", methods=["GET"])
@flask_login.login_required
def logout():
    # logoutの処理
    flask_login.logout_user()
    return flask.render_template("index.html", abs_path=get_abs)

@app.route("/dashboard", methods=["POST", "GET"])
def show_dashboard():
    # dashboardの表示
    pass

#ここからあああああ、チャットオオオオ処理
# ユーザーを全て表示
@app.route("/userlist")
def userlist():
    conn = sqlite3.connect('chattest.db')
    c = conn.cursor()
    c.execute("select id, name from user")
    user_info = c.fetchall()
    conn.close()
    return flask.render_template("userlist.html", tpl_user_info=user_info, abs_path=get_abs)


#sakorisi
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
    chat_message = request.form.get("input_message")
    conn = sqlite3.connect('chat_test.db')
    c = conn.cursor()
    c.execute("insert into chat values(?,101,?,101)",
    (reserveid, chat_message))
    conn.commit()
    c.close()
    return redirect("/chat.html/{}".format(reserveid))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)
