from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=2)])
    password = PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Zaloguj się")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=2)])
    password = PasswordField("Hasło", validators=[DataRequired()])
    password2 = PasswordField(
        "Powtórz hasło", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Zarejestruj się")
