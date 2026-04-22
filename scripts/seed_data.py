import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Domain


def run():
    app = create_app()
    with app.app_context():
        # Domaines (liste fermée)
        domains_data = ['Informatique', 'Mathématiques', 'Physique', 'Sciences de l\'ingénieur']
        for name in domains_data:
            if Domain.query.filter_by(name=name).first() is None:
                db.session.add(Domain(name=name))
                print(f'  Domaine créé : {name}')

        # Comptes de test (mot de passe : test1234)
        test_users = [
            ('admin@test.com', 'admin', 'Admin'),
            ('teacher@test.com', 'teacher', 'Enseignant'),
            ('student@test.com', 'student', 'Étudiant'),
        ]
        for email, role, label in test_users:
            if User.query.filter_by(email=email).first() is None:
                u = User(email=email, role=role)
                u.set_password('test1234')
                db.session.add(u)
                print(f'  Compte créé : {email} ({label})')

        db.session.commit()
        print('Données de test insérées.')


if __name__ == '__main__':
    run()
