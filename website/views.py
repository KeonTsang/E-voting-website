from flask import Flask, Blueprint, render_template, redirect, url_for
from.forms import CandidateForm
from.models import Candidate


app = Flask(__name__)

views = Blueprint('views', __name__)

@views.route("/")
def default():
    return render_template("Proto1.html")

@views.route("/Proto1")
def home():
    return render_template("Proto1.html")

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/candidates")
def candidates():
    return render_template("candidates.html")

@views.route("/contact")
def contact():
    return render_template("contact.html")

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/register")
def register():
    return render_template("register.html")

@views.route("/results")
def results():
    return render_template("results.html")

@views.route("/vote")
def vote():
    return render_template("vote.html")

@views.route("/admin", methods = ['GET', 'POST'])
def admin():
    candidate_form = CandidateForm()

    candidates = Candidate.query.all()

    if candidate_form.validate_on_submit():
        candidate = Candidate.query.filter_by(Name=candidate_form.Name.data).first()

        if candidate is None:

            new_name = candidate_form.Name.data

            new_party = candidate_form.Party.data

            new_con = candidate_form.Constituency.data

            Candidate.AddCandidate(new_name, new_party, new_con)

            return redirect(url_for('views.admin'))

    return render_template("admin.html", candidate_form=candidate_form, candidates = candidates)


@app.route('register', methods=['POST'])
def register():         #register function. not fully working. plan on getting variables from user entry, then adding new user to db
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']

    new_user = Register(Email=email, Password=password, Username=username)

    db.session.add(new_user)
    db.session.commit()

    return render_template("register.html", email=email, password=password, username=username)

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
