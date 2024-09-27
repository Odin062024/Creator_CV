from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileAllowed

class CVForm(FlaskForm):
    name = StringField('Imię i nazwisko', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefon', validators=[DataRequired()])
    experience = TextAreaField('Doświadczenie', validators=[DataRequired()])
    education = TextAreaField('Wykształcenie', validators=[DataRequired()])
    photo = FileField('Dodaj zdjęcie', validators=[FileAllowed(['jpg', 'png'], 'Tylko pliki obrazów!')])
    submit = SubmitField('Utwórz CV')
    template = SelectField('Wybierz szablon CV', choices=[('simple', 'Prosty'), ('modern', 'Nowoczesny')])
    submit = SubmitField('Utwórz CV')

