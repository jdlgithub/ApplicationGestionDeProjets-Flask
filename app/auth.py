"""
Authentification et autorisation par rôle.
"""
from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(*roles):
    """Décorateur : accès réservé aux rôles listés."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            if current_user.role not in roles:
                return abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator


def teacher_required(f):
    """Accès réservé aux enseignants."""
    return role_required('teacher', 'admin')(f)


def admin_required(f):
    """Accès réservé aux admins."""
    return role_required('admin')(f)


def student_required(f):
    """Accès réservé aux étudiants."""
    return role_required('student')(f)
