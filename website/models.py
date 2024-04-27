from website.__init__ import db

class Voter(db.Model):
    __tablename__ = 'Voter'
    VoterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    DateOfBirth = db.Column(db.Date)
    Username = db.Column(db.String(50))
    PasswordHash = db.Column(db.String(255))
    Salt = db.Column(db.String(50))
    IsActive = db.Column(db.Boolean)
    VoteCast = db.Column(db.Boolean)
    Admin = db.Column(db.Boolean)

# class Register(db.Model):       #creating register db. however haven't creating table into database
#     __tablename__ = 'Register'
#     Email = db.Column(db.String(255), primary_key=True, autoincrement=True)
#     Password = db.Column(db.String(255))
#     Username = db.Column(db.String(50))



class Candidate(db.Model):
    __tablename__ = 'Candidate'
    CandidateID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255))
    Party = db.Column(db.String(50))
    Constituency = db.Column(db.String(255))
    IMG_URL = db.Column(db.String(100))
    FacebookLink = db.Column(db.String(100))
    TwitterLink = db.Column(db.String(100))
    InstagramLink = db.Column(db.String(100))
    WikiLink = db.Column(db.String(100))
    descriptionLink = db.Column(db.String(255))

    @staticmethod
    def AddCandidate(Name, Party, Constituency):
        candidate = Candidate(Name=Name, Party=Party, Constituency=Constituency)
        db.session.add(candidate)
        db.session.commit()


class Vote(db.Model):
    __tablename__ = 'Vote'
    VoteID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CandidateID = db.Column(db.Integer, db.ForeignKey('Candidate.CandidateID'))

class AuditTrail(db.Model):
    __tablename__ = 'AuditTrail'
    LogID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Event = db.Column(db.String(255))
    Timestamp = db.Column(db.DateTime)
    UserID = db.Column(db.Integer)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)
