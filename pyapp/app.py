print("hello, world")

import flask
import flask_login
from collections import defaultdict

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
    # ユーザが登録済みかをチェック
    pass

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


@app.route("/login.html", methods=["POST", "GET"])
def login():
    # loginページの処理
    if(flask.request.method == "POST"):
        # ユーザーチェック
        if(flask.request.form["name"] in user_check and flask.request.form["password"] == user_check[flask.request.form["name"]]["password"]):
            # ユーザーが存在した場合はログイン
            flask_login.login_user(users.get(user_check[flask.request.form["name"]]["id"]))
            flask.flash("ログインしました", "login_success")
            return flask.render_template("dashboard.html")
        else:
            return flask.abort(401)

    return flask.render_template("login.html")

@app.route("/logout", methods=["GET"])
@flask_login.login_required
def logout():
    # logoutの処理
    flask_login.logout_user()
    return flask.render_template("index.html", abs_path=get_abs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)