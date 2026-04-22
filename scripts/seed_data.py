"""
Données de démonstration : domaines, comptes, 2 projets par domaine, étudiants et candidatures.
Idempotent : relancer le script n’ajoute pas de doublons (titres de projets et e-mails uniques).

Usage : python -m scripts.seed_data
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Application, Domain, Project, User

PASSWORD_DEMO = "test1234"

# Comptes initiaux + étudiants supplémentaires pour les candidatures
USERS_SEED = [
    ("admin@test.com", "admin"),
    ("teacher@test.com", "teacher"),
    ("student@test.com", "student"),
    ("student2@test.com", "student"),
    ("student3@test.com", "student"),
    ("student4@test.com", "student"),
    ("student5@test.com", "student"),
    ("student6@test.com", "student"),
    ("student7@test.com", "student"),
    ("student8@test.com", "student"),
]

# 2 projets par domaine : titre unique, description riche, places, statut
PROJECTS_SEED = [
    # —— Informatique ——
    {
        "domain": "Informatique",
        "title": "Plateforme web de suivi des stages",
        "description": """Conception et développement d’une application permettant aux étudiants de déposer leurs conventions, aux tuteurs entreprise de valider les objectifs et aux enseignants de suivre l’avancement (jalons, rapports intermédiaires, évaluation finale).

Livrables attendus : maquettes UX, modèle de données, API REST documentée, interface responsive et guide d’installation en local.

Technologies au choix (à valider avec l’encadrant) : stack Python/Flask ou Node, base SQL. Sensibilisation aux bonnes pratiques de sécurité (sessions, mots de passe, CSRF).""",
        "max_students": 3,
        "status": "open",
    },
    {
        "domain": "Informatique",
        "title": "Application de sensibilisation au tri des déchets",
        "description": """Projet orienté « citoyenneté numérique » : application (web ou mobile hybride) proposant quiz, cartographie des points de collecte et rappels des consignes par type de déchet pour le campus.

Vous travaillerez en lien avec le service développement durable pour recueillir le contenu pédagogique. L’accent est mis sur l’accessibilité (contraste, tailles de texte) et la clarté pour un public large.

Prérequis : bases en développement d’interface et intégration d’API cartographiques simples (fichier GeoJSON ou tuiles).""",
        "max_students": 2,
        "status": "open",
    },
    # —— Mathématiques ——
    {
        "domain": "Mathématiques",
        "title": "Modélisation statistique des flux piétons sur le campus",
        "description": """Exploitation de jeux de données réels (comptages anonymisés, horaires de cours) pour proposer un modèle prédictif des affluences aux heures de pointe. Comparaison de régressions, tests d’hypothèses et visualisations (courbes, heatmaps temporelles).

Objectifs pédagogiques : mise en forme des données, choix des variables, validation croisée, communication des limites du modèle.

Outils : Python (pandas, scikit-learn) ou R selon affinités. Un mémoire technique de 15–20 pages synthétise la démarche.""",
        "max_students": 2,
        "status": "open",
    },
    {
        "domain": "Mathématiques",
        "title": "Analyse de séries temporelles pour la consommation énergétique",
        "description": """À partir de séries historiques (données fournies, bâtiments fictifs type campus), étudier la saisonnalité, détecter des anomalies simples et proposer une courte prévision à horizon quelques semaines.

Le travail inclut une partie « nettoyage et visualisation » et une partie « modèle » (lissage exponentiel, ARIMA simplifié ou modèle de référence expliqué en cours).

Livrable : notebook commenté + rapport PDF structuré (intro, données, méthode, résultats, conclusion).""",
        "max_students": 3,
        "status": "open",
    },
    # —— Physique ——
    {
        "domain": "Physique",
        "title": "Étude et calibration d’une chaîne de mesure de température",
        "description": """Montage expérimental autour d’un capteur (type thermistance ou PT100) : schéma de conditionnement du signal, acquisition via carte d’acquisition ou microcontrôleur, étalonnage par rapport à une référence et estimation des incertitudes.

Vous rédigerez un protocole reproductible et analyserez les sources d’erreur (dérive, bruit, résolution).

Matériel mis à disposition en salle de TP ; les séances sont planifiées avec l’enseignant référent.""",
        "max_students": 2,
        "status": "open",
    },
    {
        "domain": "Physique",
        "title": "Caractérisation optique d’un dispositif à fibre optique",
        "description": """Mesure de l’atténuation sur une liaison courte, observation de la courbure minimale recommandée et comparaison avec les fiches constructeur. Introduction aux pertes par connexion et par épissure (maquette pédagogique).

Rédaction d’un compte rendu avec tableaux de mesures, graphes et discussion des incertitudes de type B.

Bon niveau en optique géométrique et en manipulation d’instrumentation souhaité.""",
        "max_students": 2,
        "status": "open",
    },
    # —— Sciences de l'ingénieur ——
    {
        "domain": "Sciences de l'ingénieur",
        "title": "Station météo autonome (maquette)",
        "description": """Conception mécanique légère du boîtier, choix des capteurs (température, humidité, pression), alimentation batterie + gestion du sommeil, transmission des données vers une base locale ou affichage sur écran.

Documentation : schémas de principe, nomenclature, budget composants et planning de réalisation.

Travail en binôme possible ; répartition des rôles électronique / mécanique à préciser en début de projet.""",
        "max_students": 4,
        "status": "open",
    },
    {
        "domain": "Sciences de l'ingénieur",
        "title": "Maquette de chaîne de traction électrique pour véhicule léger",
        "description": """Dimensionnement préliminaire d’un moteur brushless ou DC, réducteur, batterie et variateur de vitesse pour un véhicule de démonstration (petite maquette roulante). Calculs de couple, d’autonomie approximative et de dissipation thermique simplifiée.

Livrables : dossier de calcul annoté, schéma de câblage de puissance, vidéo courte de la maquette en fonctionnement (si prototype réalisé).

Encadrement sur la partie sécurité électrique (tensions faibles, fusibles).""",
        "max_students": 3,
        "status": "open",
    },
]

# (email_étudiant, titre_exact_du_projet, texte de motivation, statut candidature)
APPLICATIONS_SEED = [
    (
        "student@test.com",
        "Plateforme web de suivi des stages",
        "J’ai suivi le module développement web et je souhaite monter en compétence sur une app « métier » complète. "
        "Le suivi des stages m’intéresse car il combine gestion de documents, rôles utilisateurs et échéances. "
        "Je peux consacrer deux demi-journées par semaine au projet.",
        "pending",
    ),
    (
        "student2@test.com",
        "Plateforme web de suivi des stages",
        "Expérience en HTML/CSS et premiers pas en Python ; je veux renforcer la partie API et tests. "
        "Ce sujet correspond à mon orientation vers les métiers de développement applicatif.",
        "accepted",
    ),
    (
        "student3@test.com",
        "Plateforme web de suivi des stages",
        "Motivé par l’UX et la clarté des parcours utilisateurs. Je propose de prendre en charge les maquettes et le design system en collaboration avec les dev.",
        "pending",
    ),
    (
        "student4@test.com",
        "Application de sensibilisation au tri des déchets",
        "Engagé dans l’asso éco-campus ; je veux un support numérique concret pour nos campagnes. "
        "Idées de mini-jeux et de contenus multilingues déjà esquissés.",
        "pending",
    ),
    (
        "student5@test.com",
        "Application de sensibilisation au tri des déchets",
        "Curieux du sujet mais peu de disponibilité ce semestre ; candidature pour voir si le créneau colle.",
        "rejected",
    ),
    (
        "student@test.com",
        "Modélisation statistique des flux piétons sur le campus",
        "Solide en probas et en Python ; j’aimerais aller jusqu’à des visualisations interactives pour présenter les résultats au conseil vie étudiante.",
        "accepted",
    ),
    (
        "student6@test.com",
        "Modélisation statistique des flux piétons sur le campus",
        "Spécialité data ; je maîtrise pandas et je souhaite travailler la partie validation de modèle et intervalles de confiance.",
        "pending",
    ),
    (
        "student7@test.com",
        "Analyse de séries temporelles pour la consommation énergétique",
        "Projet aligné avec mon stage d’été dans le bâtiment tertiaire. Je veux approfondir les séries temporelles et la rédaction de prévisions exploitables.",
        "pending",
    ),
    (
        "student8@test.com",
        "Analyse de séries temporelles pour la consommation énergétique",
        "Notebook soigné et bonne culture stats ; disponible pour pair programming avec un autre candidat si besoin.",
        "pending",
    ),
    (
        "student2@test.com",
        "Étude et calibration d’une chaîne de mesure de température",
        "Passionné d’électronique et de TP ; je veux renforcer la partie incertitudes de mesure et compte rendu expérimental.",
        "pending",
    ),
    (
        "student3@test.com",
        "Caractérisation optique d’un dispositif à fibre optique",
        "Cours d’optique validés avec mention ; intéressé par les télécoms et les mesures sur banc optique.",
        "accepted",
    ),
    (
        "student4@test.com",
        "Station météo autonome (maquette)",
        "Compétences méca (CAO légère) et bricolage électronique ; je peux piloter la partie boîtier et intégration des capteurs.",
        "pending",
    ),
    (
        "student5@test.com",
        "Station météo autonome (maquette)",
        "Bon niveau en C embarqué ; je souhaite m’occuper du firmware et de la consommation en veille.",
        "pending",
    ),
    (
        "student6@test.com",
        "Station météo autonome (maquette)",
        "Candidature pour rejoindre l’équipe en support documentation et tests sur banc.",
        "pending",
    ),
    (
        "student@test.com",
        "Maquette de chaîne de traction électrique pour véhicule léger",
        "Projet véhicule électrique : je veux travailler le dimensionnement moteur/réducteur et la rédaction du dossier de calcul.",
        "pending",
    ),
    (
        "student7@test.com",
        "Maquette de chaîne de traction électrique pour véhicule léger",
        "Électronique de puissance et sécurité ; prêt à assumer la partie câblage basse tension et fusibles sous supervision.",
        "accepted",
    ),
    (
        "student8@test.com",
        "Maquette de chaîne de traction électrique pour véhicule léger",
        "Vidéo et communication du démonstrateur pour la journée portes ouvertes ; en complément d’un binôme plus calcul.",
        "pending",
    ),
]


def _ensure_user(email: str, role: str) -> User:
    u = User.query.filter_by(email=email).first()
    if u:
        return u
    u = User(email=email, role=role)
    u.set_password(PASSWORD_DEMO)
    db.session.add(u)
    db.session.flush()
    print(f"  Compte créé : {email} ({role})")
    return u


def run():
    app = create_app()
    with app.app_context():
        domains_data = [
            "Informatique",
            "Mathématiques",
            "Physique",
            "Sciences de l'ingénieur",
        ]
        for name in domains_data:
            if Domain.query.filter_by(name=name).first() is None:
                db.session.add(Domain(name=name))
                print(f"  Domaine créé : {name}")

        for email, role in USERS_SEED:
            _ensure_user(email, role)

        db.session.commit()

        teacher = User.query.filter_by(email="teacher@test.com").first()
        if not teacher:
            raise RuntimeError("Compte enseignant teacher@test.com introuvable.")

        domain_by_name = {d.name: d for d in Domain.query.all()}

        for spec in PROJECTS_SEED:
            if Project.query.filter_by(title=spec["title"]).first():
                continue
            dom = domain_by_name.get(spec["domain"])
            if not dom:
                print(f"  [AVERTISSEMENT] Domaine inconnu : {spec['domain']}, projet ignoré : {spec['title']}")
                continue
            p = Project(
                title=spec["title"],
                description=spec["description"].strip(),
                teacher_id=teacher.id,
                domain_id=dom.id,
                max_students=spec["max_students"],
                status=spec["status"],
            )
            db.session.add(p)
            print(f"  Projet créé : {spec['title']} ({spec['domain']})")

        db.session.commit()

        projects_by_title = {p.title: p for p in Project.query.all()}
        users_by_email = {u.email: u for u in User.query.filter_by(role="student").all()}

        for email, title, motivation, status in APPLICATIONS_SEED:
            student = users_by_email.get(email)
            project = projects_by_title.get(title)
            if not student or not project:
                print(f"  [AVERTISSEMENT] Candidature ignorée (utilisateur ou projet) : {email} -> {title}")
                continue
            exists = (
                Application.query.filter_by(student_id=student.id, project_id=project.id).first()
                is not None
            )
            if exists:
                continue
            db.session.add(
                Application(
                    student_id=student.id,
                    project_id=project.id,
                    motivation=motivation.strip(),
                    status=status,
                )
            )
            print(f"  Candidature : {email} -> {title} ({status})")

        db.session.commit()
        print("Données de démonstration à jour.")


if __name__ == "__main__":
    run()
