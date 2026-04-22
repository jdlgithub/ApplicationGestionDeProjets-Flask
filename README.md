# Plateforme de gestion de Projets Étudiants

Application Flask pour la gestion de projets (enseignants) et de candidatures (étudiants).

## Prérequis

- Python 3.9+
- MySQL (base de données créée au préalable)
- Variables d'environnement dans un fichier .env

## Installation

python -m venv .venv
# Windows :
.venv\Scripts\activate
# Linux / macOS :
source .venv/bin/activate

pip install -r requirements.txt
flask db upgrade

Lancer l'application avec : python app.py ou flask run

L'application est disponible sur `http://127.0.0.1:5000`.


## Premier déploiement (migrations)

Si c'est la première fois :

flask db init
flask db migrate -m "Initial"
flask db upgrade

Puis insérer les données de test (domaines + comptes) :

python -m scripts.seed_data


## Comptes de test

Après avoir exécuté python -m scripts.seed_data :

| Rôle      | Email            | Mot de passe |
|-----------|-------------------|--------------|
| Admin     | admin@test.com    | test1234     |
| Enseignant| teacher@test.com  | test1234     |
| Étudiant  | student@test.com  | test1234     |

Les domaines (Informatique, Mathématiques, Physique, etc.) sont créés automatiquement par le script.

## Structure du projet

- `app/` — package principal (models, routes, forms, auth, templates)
- `app/templates/` — base.html, auth/, projects/
- `config.py` — configuration (env, MySQL, JWT)
- `app.py` — point d'entrée

## API et endpoints

Les routes web (HTML) couvrent : inscription, connexion, liste/détail/CRUD projets, candidatures. Une documentation des endpoints REST (JSON) peut être ajoutée dans un fichier séparé pour l’API.
