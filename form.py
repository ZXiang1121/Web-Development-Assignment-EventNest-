from wtforms import Form, StringField, IntegerField, FloatField, RadioField, FileField, SelectField, TextAreaField, validators

class CreateEventForm(Form):
    event_name = StringField('Event Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    num_ticket = IntegerField('Ticket Available', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_price = FloatField('Ticket Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_date = StringField('Event Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    event_image = FileField('Event Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    description = TextAreaField('Remarks', [validators.Optional()])