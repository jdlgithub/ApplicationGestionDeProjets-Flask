"""
Formulaires WTForms (validation + CSRF).
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=8, message='Au moins 8 caractères'),
        EqualTo('password_confirm', message='Les mots de passe doivent correspondre')
    ])
    password_confirm = PasswordField('Confirmer le mot de passe', validators=[DataRequired()])
    role = SelectField('Rôle', choices=[
        ('student', 'Étudiant'),
        ('teacher', 'Enseignant'),
        ('admin', 'Administrateur'),
    ], validators=[DataRequired()])
    submit = SubmitField('Inscription')


class ProjectForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    domain_id = SelectField('Domaine', coerce=int, validators=[Optional()])
    max_students = IntegerField('Nombre max d\'étudiants', default=1, validators=[DataRequired()])
    status = SelectField('Statut', choices=[
        ('open', 'Ouvert'),
        ('closed', 'Fermé'),
        ('completed', 'Terminé'),
    ], validators=[DataRequired()])
    submit = SubmitField('Enregistrer')


class ApplicationForm(FlaskForm):
    motivation = TextAreaField('Lettre de motivation', validators=[
        DataRequired(),
        Length(min=20, message='Veuillez détailler votre motivation (au moins 20 caractères).')
    ])
    submit = SubmitField('Postuler')
