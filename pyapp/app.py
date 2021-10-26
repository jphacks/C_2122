from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import models.database as modeldb

print("hello, world")

from collections import defaultdict

import flask
import flask_login

SECRET_KEY = "secret_key"

app = flask.Flask(
        __name__,
        template_folder="static")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = SECRET_KEY

# データベース
Base = declarative_base()
app.config["SQLALCHEMY_DATABASE_URI"] = ""  # データベースのURIを入力
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
engine = create_engine(db_uri)
session_factory = sessionmaker(bind=engine)
session = session_factory()
Base.query = session.query_property()

# 今まで利用していたUserモデルと、ログイン機能用のUserMixinを合成
class LoginUser(UserMixin, modeldb.UserTable):
    # このモデルを介して認証ユーザーIDを内部で取得するためのメソッド
    def get_id(self):
        return self.id

class TestUser(flask_login.UserMixin):
    # テストユーザ用のクラス
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

users = {
    # テストユーザ
    1: TestUser(1, "user01", "password"),
    2: TestUser(2, "user02", "password")
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

"""
def load_user(user_id):
    return LoginUser.query.filter(LoginUser.id == user_id).one_or_none()
"""


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
    return flask.redirect("/")


@app.route("/dashboard", methods=["POST", "GET"])
def show_dashboard():
    # dashboardの表示
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)
