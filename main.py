# most recent python is 3.12.0(October)
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from website import views
from website import templates
from os import path





app = Flask(__name__, template_folder='e-voting/website/templates')



@app.route("/")
def home():
    return render_template("vote.html")


if __name__ == '__main__':
    app.run(debug=True)

