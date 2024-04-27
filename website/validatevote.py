from.models import Candidate, Voter, Vote, Message
from website.models import db
import datetime

def validate(voter_id):
    
    # this function verifies that the voter is eligible to cast a vote
    # returns boolean value True if they can vote, and False if not

    ageVerified = False # setting variables as their "can't vote" values by default
    voteCast = True

    # taking voter info from the DB using voterID
    voter = Voter.query.filter_by(VoterID=voter_id).first() # assumes authentication has already occured

    # age verification
    birthDate = voter.DateOfBirth
    today = datetime.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    if age >= 18:
        ageVerified = True

    # checking vote not already cast

    if voter.VoteCast == False:
        voteCast = False

    if ageVerified == True and voteCast == False:
        return True
    else:
        return False
