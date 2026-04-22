"""
Modèles SQLAlchemy : Domain, User, Project, Application.
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Domain(db.Model):
    """Domaine de projet (liste fermée)."""
    __tablename__ = 'domain'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    projects = db.relationship('Project', back_populates='domain', lazy='dynamic')

    def __repr__(self):
        return f'<Domain {self.name}>'


class User(UserMixin, db.Model):
    """Utilisateur : étudiant, enseignant ou admin."""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, teacher, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projects_created = db.relationship(
        'Project', back_populates='teacher', foreign_keys='Project.teacher_id'
    )
    applications = db.relationship(
        'Application', back_populates='student', foreign_keys='Application.student_id'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_student(self):
        return self.role == 'student'

    def __repr__(self):
        return f'<User {self.email}>'


class Project(db.Model):
    """Projet proposé par un enseignant."""
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), nullable=True)
    max_students = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='open')  # open, closed, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship('User', back_populates='projects_created', foreign_keys=[teacher_id])
    domain = db.relationship('Domain', back_populates='projects')
    applications = db.relationship('Application', back_populates='project', lazy='dynamic')

    def __repr__(self):
        return f'<Project {self.title}>'


class Application(db.Model):
    """Candidature d'un étudiant à un projet."""
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    motivation = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', back_populates='applications', foreign_keys=[student_id])
    project = db.relationship('Project', back_populates='applications')

    def __repr__(self):
        return f'<Application {self.student_id} -> {self.project_id}>'
