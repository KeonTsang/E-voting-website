from.models import Candidate, Voter, Vote, Message
from website.models import db
import datetime

def validateEligibility(voter_id):
    
    # this function verifies that the voter is eligible to cast a vote
    # returns boolean values ageVerified and voteCast so that the appropriate error message can be displayed to the user

    ageVerified = False # setting variables as their "can't vote" values by default
    voteCast = False

    # taking voter info from the DB using voterID
    voter = Voter.query.filter_by(VoterID=voter_id).first() # assumes authentication has already occured

    # age verification
    birthDate = voter.DateOfBirth
    today = datetime.date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    if age >= 18:
        ageVerified = True

    # checking that a vote has not already been cast

    if voter.VoteCast == True:
        voteCast = True

    if ageVerified == True or voteCast == False: # printing the outcome in terminal for debugging purposes
        print("Voter eligibility confirmed")
    else:
        print("Voter failed eligibility check")

    return ageVerified, voteCast
