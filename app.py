from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import json
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from os import getenv
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
app.secret_key = getenv("SECRET_KEY")
clientid = getenv("CLIENT_ID")

from database import db, Users
from utils import exchange_code, get_me, get_guilds

@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        theuser = request.form["email"]
        return check_email(theuser)

    elif request.method == "GET":
        return render_template('login.html',clientid=clientid)


@app.route('/profile')
def profile():
    email = session["user"]
    token = get_user(email)
    try:
        data = get_me(token)
        guilds = get_guilds(token)
    except Exception as err:
        if isinstance(err,HTTPError):
            Users.query.filter_by(email=email).delete()
            db.session.commit()
            flash("Not registered please sign up")
            return render_template("login.html",clientid=clientid)
    return render_template("info.html", data=data,guilds=guilds)


def check_email(email):
    usert = get_user(email)
    if usert:
        session["user"] = email
        return redirect(url_for("profile"))
    else:
        flash("Not registered please sign up")
        return render_template("login.html",clientid=clientid)


@app.route('/oauth/discord')
def oauth():
    code = request.args.get('code')
    token = exchange_code(code)
    data = get_me(token)
    print(token)
    print(data)
    user = Users(tokens=token, data=data)
    if not get_user(data["email"]):
        print("commiting")
        db.session.add(user)
        db.session.commit()
    session["user"] = data["email"]
    return redirect(url_for("profile"))


def get_user(email):
    tmp1 = Users.query.filter_by(email=email).first()
    if not tmp1:
        return None
    return json.loads(str(tmp1))


if __name__ == '__main__':
    session.clear()

    app.run(debug=True)
