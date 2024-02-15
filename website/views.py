from curses import flash
from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for
from.forms import CandidateForm
from.models import Candidate, Voter
from . import db


app = Flask(__name__)

views = Blueprint('views', __name__)

#db = SQLAlchemy()

#DB_NAME = "database.db"

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
    candidate_data = candidate.fetch_candidates()
    return render_template("candidates.html", candidates=candidate_data)

@views.route("/contact.html")
def contact():
    return render_template("contact.html")

@views.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the email and password match a user in the database
        user = Voter.query.filter_by(Username=email, PasswordHash=password).first()

        if user:
            # Log the user in
            flash("Login successful!", "success")
            return redirect(url_for("views.home"))  # Redirect to the home page or any other desired page
        else:
            flash("Invalid email or password. Please try again.", "error")

    return render_template("login.html")

# Route for handling voter registration
@views.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        dob = request.form['dob']
        username = request.form['username']
        password = request.form['password']

        # Check if the email (Address) is already in use
        existing_voter = Voter.query.filter_by(Address=address).first()
        if existing_voter:
            flash('Email is already in use. Please choose a different email.')
            return redirect(url_for('register'))

        # If the email is not in use, create a new voter
        new_voter = Voter(
            Name=name,
            Address=address,
            DateOfBirth=dob,
            Username=username,
            PasswordHash=password,  # hash the password before storing it in the database
            Salt='your_salt_value',  # Generate a unique salt for each user
            IsActive=True
        )

        db.session.add(new_voter)
        db.session.commit()

        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

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

@views.route("/admin.html", methods = ['GET', 'POST'])
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


# @app.route('register', methods=['POST'])
# def register():         #register function. not fully working. plan on getting variables from user entry, then adding new user to db
#     email = request.form['email']
#     password = request.form['password']
#     username = request.form['username']
#
#     new_user = Register(Email=email, Password=password, Username=username)
#
#     db.session.add(new_user)
#     db.session.commit()
#
#     return render_template("register.html", email=email, password=password, username=username)

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
