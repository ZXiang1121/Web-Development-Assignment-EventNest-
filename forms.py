from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators, RadioField, IntegerField
from wtforms.fields import EmailField, DateField


class signupForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    dob = DateField('Date of Birth', [validators.length(max=8), validators.Optional()])
    password = PasswordField('Password', [validators.length(max=100), validators.DataRequired()])

class loginForm(Form):
    email = EmailField('Email:', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password:', [validators.length(max=100), validators.DataRequired()])

