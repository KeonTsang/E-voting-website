from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for
from.forms import CandidateForm         #modified next 2 lines from "from.forms" and "from.models", "website."- removed the "." as wouldnt run
from.models import Candidate, Voter
from website.models import db
from encryption import *
from datetime import datetime


app = Flask(__name__)

views = Blueprint('views', __name__)

#db = SQLAlchemy()

#DB_NAME = "database.db"

@views.route("/")
def default():
    return render_template("Proto1.html")

@views.route("/Proto1.html")
def home():
    candidate_date = Candidate.query.all()
    candidate = []
    for candidate in candidate_data:
        candidate_info = {
            'name': candidate.Name,
            'party': candidate.Party,
            'constituency': candidate.Constituency,
            'img_url': candidate.IMG_URL,
            'facebook_url': candidate.facebook, #referring to models.py but not sure if db was edited in dbBrowsser to add facebook + socials columns, so implemented it in models
            'twitter_url': candidate.twitter,
            'instagram_url': candidate.insta,
            'wikipedia_url': candidate.wiki
        }
        candidate_append(candidate_info)    #dictionary of information so can use jinja
    return render_template("Proto1.html")

@views.route("/about.html")
def about():
    return render_template("about.html")

@views.route("/candidates.html")
def candidates():
    candidate_data = Candidate.query.all()
    candidate = {}
    for i in candidate_data:
        ID = i.CandidateID
        candidate[ID] = {}
        candidate[ID]["Name"] = i.Name
        candidate[ID]["Party"] = i.Party
        candidate[ID]["Constituency"] = i.Constituency
        candidate[ID]["IMG_URL"] = i.IMG_URL

    if (request.method == 'POST' and 'Name' in request.form):
        if (request.form['Name'] != None):
            c_NAME = request.form['Name']

    #    Can_name = request.args.get("Can_name")
    #    if (Can_name == None):

    return render_template("candidates.html", candidate=candidate)

@views.route("/Candidate_Base.html", methods = ["POST" , "GET"])
def Can_Page():
    Can_name = request.args.get( "Can_name" )
    if (Can_name == None):
        return render_template("Proto1.html")

    if (request.method == "POST" and "Name" in request.form):
        if (request.form["Name"]!= None):
            c_NAME = request.form["Name"]

    Searched_Can = Candidate.query.filter_by(Name = Can_name).first()
    if (Searched_Can == None):
        return render_template("Proto1.html")

    else :
        return render_template( "Candidate_Base.html" , Name=Can_name , Party = Searched_Can.Party, Constituency = Searched_Can.Constituency , Image = Searched_Can.IMG_URL)

@views.route("/contact.html")
def contact():
    return render_template("contact.html")

@views.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        voter = Voter.query.filter_by(Username=username).first()
        if voter and check_password(password, voter.PasswordHash, voter.Salt):
            # Authentication successful
            return "Login Successful"
        else:
            # If we create a 401 error page, replace the code below with the commented code
            # flash("Invalid email or password. Please try again.", "error")
            return "Invalid username or password", 401

    return render_template("login.html")

# register function with encryption. Needs testing
@views.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        # Check if the email (Address) is already in use
        existing_voter = Voter.query.filter_by(Address=address).first()
        if existing_voter:
            flash('Email is already in use. Please choose a different email.')
            return redirect(url_for('views.register'))

        #checking that the "password" and "confirm password" inputs match
    #    if password != confirm:
        #    return "Passwords do not match", 400
        #Above is already done using javascript validationForm.js

        #generating hash (see encryption.py for function)
        hashed_password, salt = generate_password_hash(password)

        #adding the newly registered user to the database
        new_voter = Voter(Name=name, Address=address, DateOfBirth=dob,
                          Username=username, PasswordHash=hashed_password, Salt=salt, IsActive=True)

        db.session.add(new_voter)
        db.session.commit()

    #    flash('Registration successful. You can now log in.')
        return redirect(url_for('views.login'))

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

    if candidate_form.is_submitted() and candidate_form.validate():
        candidate = Candidate.query.filter_by(Name=candidate_form.Name.data).first()

        if candidate is None:

            new_name = candidate_form.Name.data

            new_party = candidate_form.Party.data

            new_con = candidate_form.Constituency.data

            Candidate.AddCandidate(new_name, new_party, new_con)

            return redirect(url_for('views.admin'))

    return render_template("admin.html", candidate_form=candidate_form, candidates = candidates)


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
