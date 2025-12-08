# 2. Étude du Projet

## 2.1 Analyse de l'Existant

### 2.1.1 Reddit : Plateforme et API

**Reddit** est une plateforme de discussion et d'agrégation de contenu organisée en communautés thématiques (subreddits).

**Chiffres clés** :
- 500M+ utilisateurs actifs mensuels
- 100K+ subreddits actifs
- Millions de posts quotidiens

**Score Reddit** : Le score d'un post représente sa popularité (upvotes - downvotes)
- **Score > 1000** : Posts viraux, haute visibilité
- **Score > 100** : Discussions actives
- **Score < 100** : Posts récents, émergents

**API Reddit** :
- **PRAW** (Python Reddit API Wrapper) : Bibliothèque officielle
- **OAuth2** : Authentification sécurisée
- **Rate Limiting** : 60 requêtes/minute
- **Endpoints** : /r/{subreddit}/hot, /r/{subreddit}/new, etc.

### 2.1.2 Solutions Concurrentes

| Solution | Description | Limites |
|----------|-------------|---------|
| **Reddit natif** | Application/site officiel | Pas de filtres avancés par score, notifications basiques |
| **IFTTT/Zapier** | Automatisation no-code | Limité, coûteux pour usage intensif, pas de filtrage intelligent |
| **Pushshift** | Archive Reddit | Service arrêté en 2023 |
| **Scripts Python** | Solutions maison | Maintenance complexe, pas d'UI, non scalables |

**Constat** : Aucune solution ne combine filtrage intelligent, notifications temps réel, interface moderne et architecture scalable.

## 2.2 Étude de Faisabilité

### 2.2.1 Faisabilité Technique

✅ **Technologies matures disponibles** :
- **Backend** : FastAPI (Python) - Performance + async/await
- **Frontend** : Angular - Framework complet enterprise
- **Database** : PostgreSQL - SGBDR robuste
- **Streaming** : Kafka - Traitement événementiel
- **Containerisation** : Docker - Déploiement unifié

✅ **Compétences requises** :
- Langages : Python, TypeScript, SQL
- Frameworks : FastAPI, Angular
- DevOps : Docker, Git
- APIs : REST, WebSocket, Reddit API

✅ **Infrastructure minimale** :
- Serveur Linux (Ubuntu/Debian)
- 4GB RAM, 20GB disque
- Docker 20.10+, Docker Compose 2.0+

### 2.2.2 Faisabilité Économique

**Coûts de développement** :
- Développement : Projet de stage (2 mois)
- Outils : Technologies open-source (**0€**)
- Hébergement local : Docker sur machine existante (**0€**)
- Hébergement cloud : À partir de **10€/mois** (DigitalOcean, OVH)

**ROI estimé** :
- Gain de temps veille technologique : ~**10h/semaine**
- Détection opportunités business : **Valeur inestimable**
- Solution réutilisable et évolutive

### 2.2.3 Faisabilité Opérationnelle

✅ **Utilisateurs cibles** :
- Développeurs (veille techno)
- Entreprises (monitoring marque)
- Chercheurs (analyse données sociales)
- Marketers (tendances marché)

✅ **Facilité d'utilisation** :
- Interface web intuitive
- Pas d'installation côté client (navigateur)
- Documentation complète

✅ **Maintenance** :
- Architecture microservices modulaire
- Tests automatisés
- Logs et monitoring intégrés

## 2.3 Choix Technologiques

### 2.3.1 Stack Backend

#### FastAPI (Python 3.11+)

**Choix justifié** :
- ✅ **Performance** : Basé sur Starlette (async/await natif), comparable à Node.js
- ✅ **Documentation auto** : Swagger/ReDoc généré automatiquement
- ✅ **Validation** : Pydantic pour typage fort et validation
- ✅ **Moderne** : Support WebSocket, background tasks, dependency injection
- ✅ **Écosystème Python** : Compatible PRAW, SQLAlchemy, Pandas

**Alternatives écartées** :
- Django REST : Trop lourd, synchrone
- Flask : Moins performant, pas de validation intégrée
- Node.js/Express : Moins d'intégration avec PRAW

#### SQLAlchemy + PostgreSQL

**Choix justifié** :
- ✅ ORM mature et complet
- ✅ Support PostgreSQL (production) et SQLite (développement)
- ✅ Migration avec Alembic
- ✅ Connection pooling intégré
- ✅ Protection SQL injection

#### PRAW (Reddit API)

**Choix justifié** :
- ✅ Wrapper officiel Python pour Reddit API
- ✅ Gestion OAuth2 automatique
- ✅ Rate limiting géré en interne
- ✅ Documentation complète
- ✅ Communauté active

### 2.3.2 Stack Frontend

#### Angular 16

**Choix justifié** :
- ✅ **Framework complet** : Routing, Forms, HTTP client, Tests inclus
- ✅ **TypeScript** : Typage statique, meilleure maintenabilité
- ✅ **RxJS** : Programmation réactive idéale pour WebSocket
- ✅ **CLI puissant** : Génération de code, build optimisé
- ✅ **Enterprise-grade** : Support Google, large adoption entreprise
- ✅ **Architecture modulaire** : Components, Services, Guards

**Alternatives écartées** :
- React : Nécessite plus de bibliothèques tierces
- Vue.js : Moins d'outillage enterprise
- Svelte : Écosystème moins mature

### 2.3.3 Infrastructure

#### Docker & Docker Compose

**Choix justifié** :
- ✅ **Isolation** : Chaque service dans son conteneur
- ✅ **Reproductibilité** : Environnement identique dev/prod
- ✅ **Scalabilité** : `docker-compose scale backend=3`
- ✅ **Portabilité** : Fonctionne sur Linux/Mac/Windows
- ✅ **Orchestration** : docker-compose.yml déclaratif

#### PostgreSQL 15

**Choix justifié** :
- ✅ SGBDR open-source robuste et performant
- ✅ Support JSON pour flexibilité
- ✅ ACID compliant (transactions fiables)
- ✅ Réplication et backup
- ✅ Indexes performants

#### Apache Kafka + Zookeeper

**Choix justifié** :
- ✅ Streaming de données haute performance
- ✅ Durabilité des messages (persistance sur disque)
- ✅ Scalabilité horizontale (partitions)
- ✅ Découplage producteur/consommateur
- ✅ Standard industrie pour event streaming

## 2.4 Tableau Récapitulatif

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **Backend API** | FastAPI | 0.104.1 | Endpoints REST + WebSocket |
| **ORM** | SQLAlchemy | 2.0.23 | Accès base de données |
| **Database** | PostgreSQL | 15 | Persistance données |
| **Reddit API** | PRAW | 7.7.1 | Intégration Reddit |
| **Auth** | JWT + Bcrypt | - | Authentification sécurisée |
| **Frontend** | Angular | 16.2.0 | Interface utilisateur SPA |
| **Language** | TypeScript | 5.1.3 | Frontend typé |
| **Reactive** | RxJS | 7.8.0 | Programmation réactive |
| **Message Broker** | Kafka | latest | Streaming événements |
| **Coordination** | Zookeeper | latest | Coordination Kafka |
| **Cache** | Redis | 7 | Cache en mémoire |
| **Containerisation** | Docker | 20.10+ | Isolation services |
| **Orchestration** | Docker Compose | 2.0+ | Déploiement multi-conteneurs |
| **Reverse Proxy** | Nginx | latest | Load balancing |
| **Tests E2E** | Playwright | 1.54.1 | Tests automatisés |
