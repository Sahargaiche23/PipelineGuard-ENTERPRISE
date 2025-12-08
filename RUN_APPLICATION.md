# 🚀 PipelineGuard Enterprise - Guide de Démarrage

## 📋 Prérequis

- Docker (pour Kafka et Zookeeper)
- Python 3.8+ (pour le backend FastAPI)
- Node.js 16+ et npm (pour le frontend Angular)

## 🔧 Installation et Configuration

### 1. Démarrer Kafka et Zookeeper

```bash
# Démarrer les conteneurs Docker
docker start zookeeper
docker start kafka
```

### 2. Configurer et démarrer le Backend

```bash
# Aller dans le dossier backend
cd backend

# Installer les dépendances Python (si pas déjà fait)
pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] python-jose[cryptography] praw python-multipart

# Initialiser la base de données (créer les tables)
python init_db.py

# Démarrer le serveur FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le backend sera accessible sur **http://localhost:8000**

### 3. Démarrer le Frontend Angular

```bash
# Ouvrir un nouveau terminal
# Aller dans le dossier frontend
cd front/projet

# Installer les dépendances npm (si pas déjà fait)
npm install

# Démarrer le serveur de développement Angular
ng serve --open
```

Le frontend sera accessible sur **http://localhost:4200**

## 🎯 Fonctionnalités Disponibles

### ✅ Authentification
- **Inscription** : Créer un nouveau compte utilisateur
- **Connexion** : Se connecter avec username/password

### 👤 Gestion du Profil
- **Voir le profil** : Afficher les informations du profil
- **Modifier le profil** : 
  - Changer l'email
  - Modifier le nom complet
  - Éditer la biographie
  - **Upload d'avatar** : Télécharger une photo de profil
- **Supprimer le compte** : Supprimer définitivement son compte

### 📝 Posts et Contenu Social
- **Créer un post** :
  - Ajouter un titre et du contenu
  - **Upload d'image** : Joindre une image au post
- **Mes Posts** : Voir et gérer tous vos posts
- **Modifier un post** : Éditer le contenu de vos posts
- **Supprimer un post** : Retirer vos posts

### 🌐 Fil d'Actualité Social
- **Voir tous les posts** : Parcourir le feed de la communauté
- **Liker un post** : Cliquer sur ❤️ pour aimer un post
- **Commenter** :
  - Ajouter des commentaires sur les posts
  - Supprimer vos propres commentaires
- **Partager** : Partager un post sur votre profil

### 📊 Analytics Dashboard
- **Vue d'ensemble du compte** :
  - Âge du compte
  - Niveau d'activité (Débutant, Intermédiaire, Avancé, Expert)
  - Score d'activité total
- **Statistiques des posts** :
  - Total des posts créés
  - Likes, commentaires et partages reçus
  - Post le plus populaire
  - Timeline des 7 derniers jours
- **Statistiques des abonnements Reddit** :
  - Total des abonnements
  - Répartition par niveau (Top, Moyen, Bas)
  - Abonnements récents
- **Statistiques des notifications** :
  - Total des notifications
  - Timeline des notifications
- **Comparaison des métriques** :
  - Posts vs Abonnements vs Notifications
  - Taux d'engagement

### 🔔 Abonnements Reddit
- **S'abonner à un subreddit** : Suivre des topics Reddit
- **Filtrer par niveau** : Top, Moyen ou Bas selon le score
- **Voir les posts** : Afficher les posts de vos abonnements

### 📬 Notifications en Temps Réel
- **WebSocket** : Notifications instantanées
- **Historique** : Voir toutes vos notifications
- **Supprimer** : Nettoyer vos notifications

## 🗂️ Structure du Projet

```
PipelineGuard-ENTERPRISE/
├── backend/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── auth.py              # Authentification et profil
│   ├── posts.py             # Gestion des posts sociaux
│   ├── analytics.py         # Endpoints analytics
│   ├── models.py            # Modèles de base de données
│   ├── database.py          # Configuration SQLAlchemy
│   ├── init_db.py           # Script d'initialisation DB
│   └── config.py            # Configuration Reddit
├── front/projet/src/app/
│   ├── components/
│   │   ├── profile/         # Composant Profil
│   │   ├── my-posts/        # Composant Mes Posts
│   │   ├── analytics/       # Composant Analytics
│   │   ├── feed/            # Composant Fil d'actualité
│   │   ├── notifications/   # Composant Notifications
│   │   └── subscribe/       # Composant Abonnements
│   └── services/
│       ├── auth.service.ts
│       ├── profile.service.ts
│       ├── posts.service.ts
│       └── analytics.service.ts
```

## 🔑 Endpoints API Backend

### Authentification
- `POST /register` - Inscription
- `POST /login` - Connexion
- `GET /profile` - Obtenir le profil
- `PUT /profile` - Mettre à jour le profil
- `DELETE /profile` - Supprimer le compte

### Posts Sociaux
- `GET /posts` - Liste tous les posts
- `GET /posts/my` - Mes posts
- `POST /posts` - Créer un post
- `PUT /posts/{id}` - Modifier un post
- `DELETE /posts/{id}` - Supprimer un post
- `POST /posts/{id}/like` - Liker/Unliker
- `POST /posts/{id}/share` - Partager
- `GET /posts/{id}/comments` - Obtenir les commentaires
- `POST /posts/{id}/comments` - Ajouter un commentaire
- `DELETE /posts/{id}/comments/{comment_id}` - Supprimer un commentaire

### Analytics
- `GET /analytics/overview` - Vue d'ensemble
- `GET /analytics/posts` - Analytics des posts
- `GET /analytics/subscriptions` - Analytics des abonnements
- `GET /analytics/notifications` - Analytics des notifications
- `GET /analytics/comparison` - Comparaison des métriques

### Abonnements Reddit
- `POST /subscribe` - S'abonner à un subreddit
- `GET /my_posts` - Posts des abonnements
- `GET /search` - Rechercher dans Reddit

### Notifications
- `GET /notifications` - Liste des notifications
- `DELETE /notifications` - Supprimer toutes les notifications
- `WS /ws/{token}` - WebSocket pour notifications temps réel

## 🎨 Nouvelles Fonctionnalités Ajoutées

### 1. Système de Posts avec Images
- Upload d'images en base64
- Aperçu avant publication
- Modification et suppression

### 2. Interactions Sociales
- Système de likes avec toggle
- Commentaires avec CRUD complet
- Partage de posts sur profil

### 3. Profil Utilisateur Complet
- Avatar personnalisable
- Informations détaillées (email, nom, bio)
- Gestion du compte

### 4. Dashboard Analytics Avancé
- Visualisation de toutes les métriques
- Graphiques temporels
- Niveaux d'activité gamifiés
- Taux d'engagement

## 🔍 Navigation

Après connexion, vous pouvez accéder à:

1. **Fil d'actualité** (`/feed`) - Posts de la communauté
2. **Mes Posts** (`/my-posts`) - Gérer vos posts
3. **Analytics** (`/analytics`) - Tableau de bord
4. **Abonnements** (`/subscribe`) - Suivre des subreddits
5. **Notifications** (`/notifications`) - Notifications
6. **Profil** (`/profile`) - Gérer votre profil

## 📱 Interface Moderne

- Design Material/Modern avec gradients
- Responsive (mobile-friendly)
- Animations fluides
- Icônes emoji pour une UX conviviale
- Dark/Light accents

## 🛠️ Technologies Utilisées

### Backend
- **FastAPI** - Framework web moderne
- **SQLAlchemy** - ORM pour base de données
- **Pydantic** - Validation de données
- **JWT** - Authentification par tokens
- **PRAW** - API Reddit
- **WebSocket** - Notifications temps réel

### Frontend
- **Angular 15+** - Framework frontend
- **TypeScript** - Langage typé
- **RxJS** - Programmation réactive
- **CSS3** - Styles modernes avec gradients
- **Font Awesome** - Icônes

### Infrastructure
- **Docker** - Conteneurisation (Kafka, Zookeeper)
- **SQLite** - Base de données (peut être changée pour PostgreSQL)

## 🚨 Dépannage

### Backend ne démarre pas
```bash
# Vérifier que les dépendances sont installées
pip install -r requirements.txt

# Initialiser la base de données
python init_db.py
```

### Frontend ne démarre pas
```bash
# Réinstaller les dépendances
rm -rf node_modules package-lock.json
npm install
```

### Kafka/Zookeeper
```bash
# Vérifier que les conteneurs tournent
docker ps

# Redémarrer si nécessaire
docker restart zookeeper kafka
```

## 📝 Notes Importantes

1. **Base de données** : Les nouvelles tables (posts, comments, likes, shares) sont créées automatiquement avec `init_db.py`

2. **Images** : Les images sont stockées en base64 dans la base de données. Pour la production, envisager un système de stockage cloud (S3, etc.)

3. **Sans Docker Compose** : L'application peut tourner uniquement avec Kafka et Zookeeper en Docker, le reste en local

4. **Reddit API** : Assurez-vous que les credentials Reddit dans `config.py` sont valides

## 🎉 Félicitations!

Votre plateforme sociale PipelineGuard Enterprise est prête!

Créez un compte, uploadez un avatar, créez des posts avec images, interagissez avec la communauté et explorez vos analytics! 🚀
