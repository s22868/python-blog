from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.widgets import TextArea, EmailInput
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=2)], widget=EmailInput())
    password = PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Zaloguj się")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=2)], widget=EmailInput())
    password = PasswordField("Hasło", validators=[DataRequired()])
    password2 = PasswordField(
        "Powtórz hasło", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Zarejestruj się")

class CreatePostForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired(), Length(min=2)])
    subtitle = StringField("Podtytuł", validators=[DataRequired(), Length(min=2)])
    photo = StringField("Miniaturka", validators=[DataRequired(), Length(min=2)])
    text = StringField("Treść", validators=[DataRequired(), Length(min=10)], widget=TextArea())
    submit = SubmitField("Dodaj post")