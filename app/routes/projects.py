"""
Routes projets : liste, détail, CRUD (enseignants), candidatures.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, Application, Domain
from app.forms import ProjectForm, ApplicationForm
from app.auth import teacher_required

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/')
def list():
    """Liste publique des projets (pagination, recherche, filtre domaine)."""
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    domain_id = request.args.get('domain_id', type=int)
    query = Project.query.filter(Project.status == 'open')
    if q:
        query = query.filter(
            Project.title.ilike(f'%{q}%') | Project.description.ilike(f'%{q}%')
        )
    if domain_id:
        query = query.filter(Project.domain_id == domain_id)
    query = query.order_by(Project.created_at.desc())
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    domains = Domain.query.order_by(Domain.name).all()
    return render_template(
        'projects/list.html',
        projects=pagination.items,
        pagination=pagination,
        domains=domains,
        q=q,
        domain_id=domain_id,
    )


@projects_bp.route('/<int:project_id>')
def detail(project_id):
    """Détail d'un projet + formulaire de candidature si étudiant."""
    project = db.session.get(Project, project_id)
    if not project:
        abort(404)
    form = None
    my_application = None
    if current_user.is_authenticated and current_user.is_student:
        my_application = Application.query.filter_by(
            student_id=current_user.id, project_id=project_id
        ).first()
        if not my_application and project.status == 'open':
            form = ApplicationForm()
    return render_template(
        'projects/detail.html',
        project=project,
        form=form,
        my_application=my_application,
    )


@projects_bp.route('/new', methods=['GET', 'POST'])
@login_required
@teacher_required
def new():
    """Création d'un projet (enseignant)."""
    form = ProjectForm()
    form.domain_id.choices = [(0, '—')] + [
        (d.id, d.name) for d in Domain.query.order_by(Domain.name).all()
    ]
    if form.domain_id.data is None:
        form.domain_id.data = 0
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data or None,
            teacher_id=current_user.id,
            domain_id=form.domain_id.data or None,
            max_students=form.max_students.data,
            status=form.status.data,
        )
        db.session.add(project)
        db.session.commit()
        flash('Projet créé.', 'success')
        return redirect(url_for('projects.detail', project_id=project.id))
    return render_template('projects/form.html', form=form, project=None)


@projects_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit(project_id):
    """Modification d'un projet (enseignant, propriétaire ou admin)."""
    project = db.session.get(Project, project_id)
    if not project:
        abort(404)
    if project.teacher_id != current_user.id and not current_user.is_admin:
        abort(403)
    form = ProjectForm(obj=project)
    form.domain_id.choices = [(0, '—')] + [
        (d.id, d.name) for d in Domain.query.order_by(Domain.name).all()
    ]
    if form.domain_id.data is None:
        form.domain_id.data = 0
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data or None
        project.domain_id = form.domain_id.data or None
        project.max_students = form.max_students.data
        project.status = form.status.data
        db.session.commit()
        flash('Projet mis à jour.', 'success')
        return redirect(url_for('projects.detail', project_id=project.id))
    return render_template('projects/form.html', form=form, project=project)


@projects_bp.route('/<int:project_id>/apply', methods=['POST'])
@login_required
def apply(project_id):
    """Postuler à un projet (étudiant)."""
    if not current_user.is_student:
        abort(403)
    project = db.session.get(Project, project_id)
    if not project or project.status != 'open':
        abort(404)
    existing = Application.query.filter_by(
        student_id=current_user.id, project_id=project_id
    ).first()
    if existing:
        flash('Vous avez déjà postulé à ce projet.', 'warning')
        return redirect(url_for('projects.detail', project_id=project_id))
    form = ApplicationForm()
    if form.validate_on_submit():
        app = Application(
            student_id=current_user.id,
            project_id=project_id,
            motivation=form.motivation.data,
            status='pending',
        )
        db.session.add(app)
        db.session.commit()
        flash('Candidature envoyée.', 'success')
        # TODO: notification email simulée
    else:
        for field, errors in form.errors.items():
            for e in errors:
                flash(e, 'danger')
    return redirect(url_for('projects.detail', project_id=project_id))


@projects_bp.route('/<int:project_id>/applications')
@login_required
@teacher_required
def applications(project_id):
    """Liste des candidatures pour un projet (enseignant)."""
    project = db.session.get(Project, project_id)
    if not project:
        abort(404)
    if project.teacher_id != current_user.id and not current_user.is_admin:
        abort(403)
    apps = Application.query.filter_by(project_id=project_id).order_by(Application.applied_at.desc()).all()
    return render_template('projects/applications.html', project=project, applications=apps)


@projects_bp.route('/applications/<int:app_id>/<action>', methods=['POST'])
@login_required
@teacher_required
def application_action(app_id, action):
    """Accepter ou refuser une candidature."""
    if action not in ('accept', 'reject'):
        abort(400)
    app = db.session.get(Application, app_id)
    if not app:
        abort(404)
    if app.project.teacher_id != current_user.id and not current_user.is_admin:
        abort(403)
    app.status = 'accepted' if action == 'accept' else 'rejected'
    db.session.commit()
    flash('Candidature mise à jour.', 'success')
    # TODO: notification email simulée
    return redirect(url_for('projects.applications', project_id=app.project_id))
