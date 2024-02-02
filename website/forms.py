from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class CandidateForm(FlaskForm):
    Name = StringField('Name', validators=[InputRequired()])
    Party = StringField('Party', validators=[InputRequired()])
    Constituency = StringField('Constituency', validators=[InputRequired()])
    submit = SubmitField('Submit')