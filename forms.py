from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators,DateField, TimeField, FileField, RadioField, IntegerField, BooleanField, SubmitField
from wtforms.fields import EmailField, DateField
from flask_wtf import FlaskForm


class signupForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    birthdate = DateField('Date of Birth', [validators.length(max=8), validators.Optional()])
    password = PasswordField('Password', [validators.Length(min=8, max=20), validators.DataRequired()]) 

class loginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(max=100), validators.DataRequired()])


# no html link yet
class changPw(Form):
    newpassword = PasswordField('New Password', [validators.length(max=100), validators.DataRequired()])

class forgetpw(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])


# parik part. (ZX) I will do some but need someone to help me with upload image ...
class createEvent(Form):
    event_name = StringField('Event Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_category = SelectField('Event Category', [validators.DataRequired()], choices=[('', 'Select'), ('S', 'Sport'), ('C', 'Concert')], default='')
    event_date = DateField('Event Date',  [validators.DataRequired()], format='%Y-%m-%d')
    event_time = TimeField('Event Time', [validators.DataRequired()], format='%H:%M')
    event_location = StringField('Event Location', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_image = FileField('Image')
    event_desc = TextAreaField('Description', [validators.DataRequired()])


class ContactForm(FlaskForm):
    name = TextAreaField("Name")
    email = TextAreaField("Email")
    number =  TextAreaField("number")
    subject = TextAreaField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")