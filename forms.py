from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class CVForm(FlaskForm):
    name = StringField('Imię i nazwisko', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefon', validators=[DataRequired()])
    experience = TextAreaField('Doświadczenie', validators=[DataRequired()])
    education = TextAreaField('Wykształcenie', validators=[DataRequired()])
    submit = SubmitField('Utwórz CV')
