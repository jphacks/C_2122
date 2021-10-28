import datetime
import sqlite3
import flask
import flask_login

SECRET_KEY = "secret_key"

app = flask.Flask(
    __name__,
    template_folder="static")
app.config["SECRET_KEY"] = SECRET_KEY
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
user_id = 0

# ログイン用のクラス


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
            user_id = int(user[0][0])
            flask_login.login_user(User(int(user[0][0])))
            print("login success")
            return flask.redirect("room.html")
        else:
            print("login fail : Name or password does not match")
            print(user)
            flask.flash("ユーザー名またはパスワードが間違っています", "sign in fail")
            return flask.redirect("login.html")
    return flask.render_template("login.html", abs_path=get_abs)


@app.route("/signup.html", methods=["POST", "GET"])
def sign_up():
    # loginページの処理
    if(flask.request.method == "POST"):
        # ユーザーチェック
        conn = sqlite3.connect('chat_test.db')
        c = conn.cursor()
        if len(flask.request.form["name"]) < 2:
            flask.flash("ユーザー名が短すぎます", "name is too short.")
            return flask.redirect("/signup.html")
        if len(flask.request.form["password"]) < 2:
            flask.flash("パスワードが短すぎます", "password is too short.")
            return flask.redirect("/signup.html")
        try:
            c.execute(
                "select * from user where username = '{}' ".format(flask.request.form["name"]))
            user = c.fetchall()
            if user == []:
                raise "NoData"
            flask.flash("その名前はすでに使用されています", "sign up fail")
            return flask.redirect("/signup.html")
        except:
            c.execute(
                "insert into user(username, password) values('{}', '{}')".format(
                    flask.request.form["name"], flask.request.form["password"])
            )
            print("Sign up success")
            c.execute(
                "select * from user where username = '{}' ".format(flask.request.form["name"]))
            user = c.fetchall()
            print(user)
            conn.commit()
            conn.close()
            flask_login.login_user(User(int(user[0][0])))
            return flask.redirect("room.html")
    return flask.render_template("signup.html", abs_path=get_abs)


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
    user_id = flask_login.current_user.get_id()  # ログインしているユーザのidを取得
    c.execute(
        "select reserve.id, purpose.content from reserve inner join purpose on (reserve.purpose_id1 = purpose.id) or (reserve.purpose_id2 = purpose.id) where purpose.user_id = {}".format(user_id))
    room_list = c.fetchall()
    conn.close()
    return flask.render_template("room.html", tpl_room_list=room_list, abs_path=get_abs)


@app.route("/chat.html/<int:reserveid>")
def chat(reserveid):
    user_id = flask_login.current_user.get_id()
    conn = sqlite3.connect('chat_test.db')
    c = conn.cursor()
    c.execute(
        "select reserve_id, date, content, user_id_sender from chat where reserve_id = {}".format(reserveid))
    chat_fetch = c.fetchall()
    chat_list = []
    for chat in chat_fetch:
        chat_list.append(
            {"reserve_id": chat[0], "date": chat[1],
                "content": chat[2], "user_id": chat[3]}
        )
    c.close()
    return flask.render_template("chat.html", chat_list=chat_list, reserve_id=reserveid, user_id=user_id, abs_path=get_abs)


@app.route("/chat.html/<int:reserveid>", methods=["POST"])
def chat_post(reserveid):
    user_id = flask_login.current_user.get_id()
    chat_message = flask.request.form.get("input_message")
    conn = sqlite3.connect('chat_test.db')
    c = conn.cursor()
    c.execute("insert into chat values(?,?,?,?)", (reserveid,
            datetime.datetime.now(), chat_message, user_id))
    conn.commit()
    c.close()
    return flask.redirect("/chat.html/{}".format(reserveid))


#予約処理


@app.route("/reservation.html", methods=["POST", "GET"])
@flask_login.login_required
def reserve():
    """
    conn = sqlite3.connect('reserve_test.db')
    c = conn.cursor()
    c.execute('CREATE TABLE reserve (id integer, date text, time text, purpose text)')
    conn.commit()
    conn.close()
    return flask.render_template('<reserve {}>', abs_path=get_abs)"""
    if(flask.request.method == "POST"):
        # ユーザーチェック
        conn = sqlite3.connect('chat_test.db')
        c = conn.cursor()
        user_id = flask_login.current_user.get_id()
        print(flask.request.form)
        t = flask.request.form["time"].replace(":", "-")
        c.execute("insert into purpose(date, user_id, content) values('{}', '{}', '{}')".format(
            str(flask.request.form["date"]) + "-" + t, user_id, flask.request.form["purpose"]))
        conn.commit()
        c.execute(
            "select reserve.id, purpose.content from reserve inner join purpose on (reserve.purpose_id1 = purpose.id) or (reserve.purpose_id2 = purpose.id) where purpose.user_id = {}".format(user_id))
        room_list = c.fetchall()
        print(room_list)
        c.close()
        return flask.render_template("/reservation.html", abs_path=get_abs, messages=room_list)
    return flask.render_template("/reservation.html", abs_path=get_abs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)
