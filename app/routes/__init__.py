"""
Routes principales (accueil, dashboard).
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.auth import role_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Page d'accueil : redirection selon rôle ou liste des projets."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('projects.list'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord selon le rôle."""
    return render_template('dashboard.html')
