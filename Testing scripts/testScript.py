import random
from datetime import datetime, timedelta

import requests
from flask import redirect, render_template, request, url_for

from website import views
from website.forms import CandidateForm
from website.models import Candidate, Voter, db

#Need to add voting URL

@views.route("/adminvote.html", methods=['GET', 'POST'])
def adminvote():
    candidate_form = CandidateForm()

    candidates = Candidate.query.all()

    if request.method == 'POST':
        if request.form.get('run_testing_script'): #Get inputs from html page to set voter numbers
            num_fake_voters = 50
            num_test_votes = 100

            # Simulate voter registration
            fake_results_reg = simulate_voter_registration(num_fake_voters)

            # Simulate casting test votes
            fake_results_vote = simulate_test_votes(num_test_votes)

            
            

            # Pass the results to the template
            return render_template("admin.html", candidate_form=candidate_form, candidates=candidates, reg_results=fake_results_reg, vote_results = fake_results_vote)

    return render_template("admin.html", candidate_form=candidate_form, candidates=candidates, results=None)

# Function to generate a fake voter
def generate_fake_voter():
    username = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8))
    name = 'Fake User ' + username
    address = username + '@example.com'
    dob = datetime.utcnow() - timedelta(days=random.randint(365 * 18, 365 * 70))  # Random age between 18 and 70 years
    password = 'fakepassword'  

    return name, address, dob, username, password

# Function to simulate voter registration
def simulate_voter_registration(num_fake_voters):
    for _ in range(num_fake_voters):
        name, address, dob, username, password = generate_fake_voter()

        voter = Voter(Name=name, Address=address, DateOfBirth=dob,Username=username, PasswordHash=password, IsActive=True)


# Function to simulate casting test votes
def simulate_test_votes(num_votes):
    voters = Voter.query.all()
    candidates = Candidate.query.all()

    for _ in range(num_votes):
        random_voter = random.choice(voters)
        random_candidate = random.choice(candidates)

        payload = {'VoterID': random_voter.VoterID, 'CandidateID': random_candidate.CandidateID}

        try:
            response = requests.post("/results.html", data=payload)
            if response.status_code == 200:
                print(f"Vote successful for voter {random_voter.Username} to candidate {random_candidate.Name}")
            else:
                print(f"Failed to vote for voter {random_voter.Username} to candidate {random_candidate.Name}, "f"Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error voting for voter {random_voter.Username} to candidate {random_candidate.Name}, Exception: {e}")
