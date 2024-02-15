from flask import Flask, Blueprint, render_template

app = Flask(__name__)

views = Blueprint('views', __name__)

@views.route("/")
def default():
    return render_template("Proto1.html")

@views.route("/Proto1.html")
def home():
    return render_template("Proto1.html")

@views.route("/about.html")
def about():
    return render_template("about.html")

@views.route("/candidates.html")
def candidates():
    return render_template("candidates.html")

@views.route("/contact.html")
def contact():
    return render_template("contact.html")

@views.route("/login.html")
def login():
    return render_template("login.html")

@views.route("/register.html")
def register():
    return render_template("register.html")

@views.route("/results.html")
def results():
    return render_template("results.html")

@views.route("/vote.html")
def vote():
    return render_template("vote.html")
@views.route("/Joe.html")
def Joe():
    return render_template("Joe.html")

@views.route("/Boris.html")
def Boris():
    return render_template("Boris.html")

@views.route("/Donald.html")
def Donald():
    return render_template("Donald.html")

@views.route("/Rishi.html")
def Rishi():
    return render_template("Rishi.html")


# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template("Errors/404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500



# Register the blueprint with the Flask app
app.register_blueprint(views)

if __name__ == '__main__':
    app.run(debug=True)
