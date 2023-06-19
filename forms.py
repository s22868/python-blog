from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=2)])
    password = PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Zaloguj się")


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=2)])
    password = PasswordField("Hasło", validators=[DataRequired()])
    password2 = PasswordField(
        "Powtórz hasło", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Zarejestruj się")

class ForgotPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=2)])
    submit = SubmitField("Zresetuj hasło")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Hasło", validators=[DataRequired()])
    password2 = PasswordField(
        "Powtórz hasło", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Zmień hasło")

class CreatePostForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired(), Length(min=2)])
    subtitle = StringField("Podtytuł", validators=[DataRequired(), Length(min=2)])
    photo = StringField("Miniaturka", validators=[DataRequired(), Length(min=2)])
    text = TextAreaField("Treść", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Dodaj post")

class EditPostForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired(), Length(min=2)])
    subtitle = StringField("Podtytuł", validators=[DataRequired(), Length(min=2)])
    photo = StringField("Miniaturka", validators=[DataRequired(), Length(min=2)])
    text = TextAreaField("Treść", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Edytuj post")
