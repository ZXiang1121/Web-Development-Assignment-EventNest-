from wtforms import Form, StringField, IntegerField, FloatField, FileField, RadioField, SelectField, TextAreaField, validators

class CreateEventForm(Form):
    event_name = StringField('Event Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    num_ticket = IntegerField('Ticket Available', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_location = StringField('Event Location', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_price = FloatField('Ticket Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    seat_type = StringField('Event Seating', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_date = StringField('Event Name', [validators.Length(min=1, max=150), validators.DataRequired()])

    # event_image = FileField('Event Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    description = TextAreaField('Remarks', [validators.Optional()])