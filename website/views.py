import os

from flask import jsonify
from flask import (Blueprint, Flask, flash, redirect, render_template, request,
                   session, url_for)

from.forms import CandidateForm         #modified next 2 lines from "from.forms" and "from.models", "website."- removed the "." as wouldnt run
from.models import Candidate, Voter, Vote, Message
import secrets
from collections import defaultdict
from datetime import datetime

import pyotp
import qrcode

from website.encryption import *
from website.validatevote import validateEligibility
from website.models import db

app = Flask(__name__)

views = Blueprint('views', __name__)

#db = SQLAlchemy()

#DB_NAME = "database.db"

@views.route("/")
def default():
    return render_template("Proto1.html")

@views.route("/Proto1.html")
def home():
    candidate_info = Candidate.query.all()
    candidate = {}
    for candidate in candidate_info:
        candidate_info = {
            'name': candidate.Name,
            'party': candidate.Party,
            'constituency': candidate.Constituency,
            'img_url': candidate.IMG_URL,
            'facebook_url': candidate.FacebookLink, #referring to models.py but not sure if db was edited in dbBrowsser to add facebook + socials columns, so implemented it in models
            'twitter_url': candidate.TwitterLink,
            'instagram_url': candidate.InstagramLink,
            'wikipedia_url': candidate.WikiLink
        }
        #candidate.update(candidate_info)    #dictionary of information so can use jinja
    return render_template("Proto1.html" , candidate = candidate)

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
        candidate[ID]["FacebookLink"] = i.FacebookLink
        candidate[ID]["TwitterLink"] = i.TwitterLink
        candidate[ID]["InstagramLink"] = i.InstagramLink
        candidate[ID]['WikiLink'] = i.WikiLink

    print("Candidates:", candidate_data)
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
        return render_template( "Candidate_Base.html" , Name=Can_name , Party = Searched_Can.Party, Constituency = Searched_Can.Constituency , Image = Searched_Can.IMG_URL , Facebook = Searched_Can.FacebookLink , Insta = Searched_Can.InstagramLink , Wiki = Searched_Can.WikiLink , Twitter = Searched_Can.TwitterLink)

@views.route("/contact.html", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        message_text = request.form['message']

        message = Message(fname=fname, lname=lname, email=email, message=message_text)
        db.session.add(message)
        db.session.commit()
    return render_template("contact.html")

@views.route("/messages.html")
def messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)

@views.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        voter = Voter.query.filter_by(Username=username).first()
        if voter and check_password(password, voter.PasswordHash, voter.Salt):
            # Authentication successful
            session['user_id'] = voter.VoterID  # Store user ID in the session
            return redirect(url_for('views.vote', noselection=False))
        else:
            return "Invalid username or password", 401

    return render_template("login.html")




# Function to generate secret key for Google Authenticator
def generate_secret_key():
    return pyotp.random_base32()

@views.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        # Store registration information in the session
        session['registration_data'] = {
            'name': name,
            'address': address,
            'dob': dob,
            'username': username,
            'password': password,
            
        }

        # Check if the email (Address) is already in use
        existing_voter = Voter.query.filter_by(Address=address).first()
        if existing_voter:
            print('Email is already in use. Please choose a different email.')
            return redirect(url_for('views.register'))

        # Generate secret key for Google Authenticator
        secret_key = generate_secret_key()
        print(secret_key)
        session['secret_key'] = secret_key

        totp_auth = pyotp.totp.TOTP( 
            secret_key).provisioning_uri( 
            name=username, 
            issuer_name='E-Voting') 

        # Define the folder where you want to save the QR code image
        UPLOAD_FOLDER = 'website/static/qr_codes'

        # Ensure the folder exists, create it if necessary
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Construct the filename for the QR code image based on the username
        qr_filename = f"{username}_qr.png"

        # Generate the QR code with the constructed filename
        qr_path = os.path.join(UPLOAD_FOLDER, qr_filename)
        qrcode.make(totp_auth).save(qr_path)

        # Render registration page with QR code filename
        return render_template('registerQR.html', qr_name=qr_filename)

    return render_template('register.html')


@views.route('/verify_registration', methods=['GET', 'POST'])
def verify_registration():
    if request.method == 'POST':
        user_entered_code = request.form['verification_code']
        secret_key = session.get('secret_key')

        if not secret_key:
            flash('Secret key not found. Please register again.')
            return redirect(url_for('views.register'))

        # Retrieve registration data from the session
        registration_data = session.get('registration_data')

        if not registration_data:
            flash('Registration data not found. Please register again.')
            return redirect(url_for('views.register'))

        name = registration_data['name']
        address = registration_data['address']
        dob = registration_data['dob']
        username = registration_data['username']
        password = registration_data['password']

        # Verify the entered code
        print(secret_key)
        totp = pyotp.TOTP(secret_key)
        if totp.verify(user_entered_code):
            # Code is valid, proceed with registration
            
            # Generate password hash
            hashed_password, salt = generate_password_hash(password)

            # Add the newly registered user to the database
            new_voter = Voter(
                Name=name, Address=address, DateOfBirth=dob,
                Username=username, PasswordHash=hashed_password, Salt=salt,
                IsActive=True, VoteCast = False, Admin = False # these 3 are default values for every new voter
            )

            db.session.add(new_voter)
            db.session.commit()

             # Clear session data related to registration
            session.pop('registration_data')
            session.pop('secret_key')
            
            # Update session with user ID
            session['user_id'] = new_voter.VoterID
            
            # Redirect to login page
            return redirect(url_for('views.login'))
        else:
            print('Invalid verification code. Please try again.')
            return redirect(url_for('views.register'))


    return render_template('register.html')



@views.route('/check_email_availability')
def check_email_availability():
    email = request.args.get('email')

    if email:
        existing_voter = Voter.query.filter_by(Address=email).first()
        if existing_voter:
            return jsonify({"exists": True})
        else:
            return jsonify({"exists": False})
    else:
        # Handle case where no email parameter is provided
        return jsonify({"error": "No email provided"})



@views.route("/results.html")
def results():
    vote_info = Vote.query.all()
    candidate_votes = defaultdict(int)
    for vote in vote_info:
        candidate_votes[vote.CandidateID] += 1
    candidate_info = Candidate.query.all()
    candidates = []
    for candidate in candidate_info:
        candidates.append({
            'name': candidate.Name,
            'votes': candidate_votes.get(candidate.CandidateID, 0)  # Get total votes for each candidate
    })
    return render_template("results.html", candidates=candidates)

@views.route("/vote.html/<noselection>") 
# to redirect to this page, use return redirect(url_for('views.vote', noselection=False))

# noselection is set to True when the user has been returned to the vote page because they did not select a
# candidate when they pressed the vote button

def vote(noselection): # beware!! noselection is a string, not a boolean
    if 'user_id' in session:
        candidate_list = Candidate.query.all()
        if noselection == "True":
            return render_template("vote.html", noselection=True, user_authenticated=True, candidate_list=candidate_list) #This needs to pass the user not just if they are authenticated
        else:
            return render_template("vote.html", noselection=False, user_authenticated=True, candidate_list=candidate_list) #This needs to pass the user not just if they are authenticated
    else:
        return render_template("vote.html", user_authenticated=False)

@views.route("/submit_vote", methods=["POST"])
def submit_vote():
    if 'user_id' in session:
        voted_candidate_id = request.form.get('voted_candidate')
        voter_id = session['user_id']

        if voted_candidate_id != "":
            print(voted_candidate_id) # displays the candidate the user voted for the terminal, purely for debugging

        if voted_candidate_id == None:
            return redirect(url_for("views.vote", noselection = True))

        # vote eligibility check
        ageVerified, voteCast = validateEligibility(voter_id)
        if ageVerified == False:
            return "Error: You must be 18 or older to cast a vote in this election.", 401
        if voteCast == True:
            return "Error: You have already voted in this election and may not vote again.", 401


        # Save the vote
        vote = Vote(CandidateID=voted_candidate_id)
        # marking that the voter has voted in the "Voter" database
        voter = Voter.query.get(voter_id)
        voter.VoteCast = True
        db.session.add(vote)
        db.session.commit()

        session["voted_candidate_id"] = voted_candidate_id

        return redirect(url_for('views.vote_confirmation'))  # Redirect to success page
    else:
        return "You must be logged in to vote.", 401
    
@views.route('/vote_confirmation')
def vote_confirmation():
    if 'voted_candidate_id' in session:
        candidate_id = session['voted_candidate_id']
        #get candidate details by their ID
        candidate = Candidate.query.filter_by(CandidateID=candidate_id).first()
        candidate_name = candidate.Name
        candidate_party = candidate.Party
    else:
        # Redirect to home if there's no candidate_id in the session
        return render_template("Proto1.html")

    return render_template('vote_confirmation.html', candidate_name=candidate_name, candidate_party=candidate_party)


@views.route("/Joe.html")
def Joe():
    candidate = Candidate.query.first()

    with open(candidate.descriptionLink, 'r') as file:
        text = file.read()
    return render_template("Joe.html", text=text)

@views.route("/Boris.html")
def Boris():
    candidate = Candidate.query.first()
    with open(candidate.descriptionLink, 'r') as file:
        text = file.read()
    return render_template("Boris.html" , text=text)

@views.route("/Donald.html")
def Donald():
    candidate = Candidate.query.first()
    with open(candidate.descriptionLink, 'r') as file:
        text = file.read()
    return render_template("Donald.html",  text=text)

@views.route("/Rishi.html")
def Rishi():
    candidate = Candidate.query.first()
    with open(candidate.descriptionLink, 'r') as file:
        text = file.read()
    return render_template("Rishi.html", text=text)

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
    app.run(debug=True)
