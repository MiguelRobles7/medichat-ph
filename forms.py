from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField, BooleanField


class GeneralForm(FlaskForm):
    gender = StringField('Sex')
    bmi = IntegerField('BMI')
    age = IntegerField('Age')
    submit_field = SubmitField('CONTINUE >>')


class SymptomsForm(FlaskForm):
    symptoms = RadioField('Symptoms', choices=[('Yes', 'Yes'), ('No', 'No')])
    next_button = SubmitField('Next')
