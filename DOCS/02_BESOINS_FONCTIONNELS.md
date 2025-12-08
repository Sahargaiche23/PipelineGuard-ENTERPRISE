# 📋 PipelineGuard Enterprise - Besoins Fonctionnels

## 📝 Catalogue des Besoins Fonctionnels

### **BF1 - Gestion des Utilisateurs**

#### BF1.1 : Inscription
- **Description** : Permettre à un nouvel utilisateur de créer un compte
- **Endpoint** : `POST /register`
- **Paramètres** : username, password
- **Validation** : 
  - Username unique
  - Password non vide
- **Résultat** : Compte créé, mot de passe haché avec Bcrypt
- **Statut** : ✅ Implémenté

#### BF1.2 : Connexion
- **Description** : Authentifier un utilisateur existant
- **Endpoint** : `POST /login`
- **Paramètres** : username, password
- **Validation** : Vérification du mot de passe haché
- **Résultat** : Token JWT valide 30 minutes
- **Statut** : ✅ Implémenté

#### BF1.3 : Consultation du profil
- **Description** : Récupérer les informations de l'utilisateur connecté
- **Endpoint** : `GET /profile`
- **Authentification** : JWT requis
- **Données retournées** : id, username, email, full_name, bio, avatar, created_at
- **Statut** : ✅ Implémenté

#### BF1.4 : Modification du profil
- **Description** : Mettre à jour les informations personnelles
- **Endpoint** : `PUT /profile`
- **Authentification** : JWT requis
- **Paramètres optionnels** : email, full_name, bio, avatar_base64
- **Validation** : Email unique si fourni
- **Statut** : ✅ Implémenté

#### BF1.5 : Upload d'avatar
- **Description** : Télécharger une photo de profil
- **Format** : Base64 encodé (inclus dans BF1.4)
- **Stockage** : Colonne avatar_base64 dans la base
- **Affichage** : Décodage automatique dans le frontend
- **Statut** : ✅ Implémenté

#### BF1.6 : Suppression de compte
- **Description** : Supprimer définitivement son compte
- **Endpoint** : `DELETE /profile`
- **Authentification** : JWT requis
- **Cascade** : Supprime posts, comments, likes, shares, subscriptions, notifications
- **Irréversible** : Confirmation requise dans l'UI
- **Statut** : ✅ Implémenté

---

### **BF2 - Abonnements Reddit**

#### BF2.1 : Recherche de subreddits
- **Description** : Chercher un subreddit par nom et prévisualiser les posts
- **Endpoint** : `GET /search?q=<subreddit_name>`
- **Authentification** : JWT requis
- **Validation** : 
  - Vérification de l'existence du subreddit
  - Gestion des subreddits privés/inexistants
- **Résultat** : Liste de 20 posts (hot) avec score, auteur, URL
- **Statut** : ✅ Implémenté

#### BF2.2 : S'abonner à un subreddit
- **Description** : Créer un abonnement avec niveau de filtrage
- **Endpoint** : `POST /subscribe`
- **Paramètres** : 
  - `topic` : nom du subreddit
  - `level` : "top", "moyen", ou "bas"
- **Validation** : Niveau doit être valide
- **Actions** :
  1. Créer l'abonnement en base
  2. Créer une notification
  3. Envoyer notification via WebSocket
- **Statut** : ✅ Implémenté

#### BF2.3 : Lister ses abonnements
- **Description** : Voir tous ses abonnements actifs
- **Endpoint** : `GET /analytics/subscriptions`
- **Authentification** : JWT requis
- **Données retournées** :
  - Total d'abonnements
  - Répartition par niveau (top/moyen/bas)
  - Liste des 5 abonnements récents
- **Statut** : ✅ Implémenté

#### BF2.4 : Consulter les posts filtrés
- **Description** : Voir les posts correspondant à ses abonnements
- **Endpoint** : `GET /my_posts`
- **Authentification** : JWT requis
- **Filtrage** : Uniquement les posts du niveau abonné
- **Résultat** : Posts avec topic, level, score, URL, auteur
- **Statut** : ✅ Implémenté

#### BF2.5 : Se désabonner
- **Description** : Supprimer un abonnement
- **Méthode** : Suppression directe en base (DELETE via analytics)
- **Authentification** : JWT requis
- **Statut** : ⚠️ À implémenter explicitement

---

### **BF3 - Système de Notifications**

#### BF3.1 : Connexion WebSocket
- **Description** : Établir une connexion temps réel pour les notifications
- **Endpoint** : `WS /ws/{jwt_token}`
- **Authentification** : JWT dans l'URL
- **Actions initiales** :
  1. Validation du token
  2. Envoi de toutes les notifications existantes
  3. Démarrage de la boucle de surveillance (polling 5s)
- **Statut** : ✅ Implémenté

#### BF3.2 : Notification d'abonnement
- **Description** : Recevoir une notification lors d'un nouvel abonnement
- **Trigger** : Création d'un Subscription
- **Format** : "Abonnement au topic '{topic}' niveau '{level}'"
- **Canal** : WebSocket + historique en DB
- **Statut** : ✅ Implémenté

#### BF3.3 : Historique des notifications
- **Description** : Consulter l'historique complet
- **Endpoint** : `GET /notifications`
- **Authentification** : JWT requis
- **Tri** : Par date décroissante (plus récentes en premier)
- **Format** : id, title, content, url, created_at
- **Statut** : ✅ Implémenté

#### BF3.4 : Supprimer toutes les notifications
- **Description** : Vider l'historique de notifications
- **Endpoint** : `DELETE /notifications`
- **Authentification** : JWT requis
- **Action** : Suppression en cascade de toutes les notifications de l'utilisateur
- **Statut** : ✅ Implémenté

#### BF3.5 : Format structuré
- **Structure JSON** :
```json
{
  "id": 123,
  "title": "Notification Reddit",
  "content": "Abonnement au topic 'python' niveau 'top'",
  "url": "",
  "created_at": "2025-11-04T10:30:00"
}
```
- **Statut** : ✅ Implémenté

---

### **BF4 - Gestion de Contenu**

#### BF4.1 : Créer un post
- **Description** : Publier un nouveau post
- **Endpoint** : `POST /posts`
- **Authentification** : JWT requis
- **Paramètres** :
  - `title` : Obligatoire
  - `content` : Optionnel
  - `image_base64` : Optionnel
- **Statut** : ✅ Implémenté

#### BF4.2 : Fil d'actualités
- **Description** : Voir tous les posts de la plateforme
- **Endpoint** : `GET /posts`
- **Authentification** : JWT requis
- **Pagination** : skip=0, limit=50
- **Tri** : Par date décroissante
- **Enrichissement** : Avatar de l'auteur, statut like
- **Statut** : ✅ Implémenté

#### BF4.3 : Liker un post
- **Description** : Aimer/Ne plus aimer un post
- **Endpoint** : `POST /posts/{post_id}/like`
- **Authentification** : JWT requis
- **Toggle** : Si déjà liké → unlike, sinon → like
- **Compteur** : Incrémente/Décrémente likes_count
- **Statut** : ✅ Implémenté

#### BF4.4 : Commenter
- **Description** : Ajouter un commentaire sur un post
- **Endpoint** : `POST /posts/{post_id}/comments`
- **Authentification** : JWT requis
- **Paramètre** : content (obligatoire)
- **Compteur** : Incrémente comments_count du post
- **Statut** : ✅ Implémenté

#### BF4.5 : Partager un post
- **Description** : Partager sur son profil
- **Endpoint** : `POST /posts/{post_id}/share`
- **Authentification** : JWT requis
- **Action** : Crée un Share, incrémente shares_count
- **Statut** : ✅ Implémenté

#### BF4.6 : Modifier son post
- **Description** : Éditer un post existant
- **Endpoint** : `PUT /posts/{post_id}`
- **Authentification** : JWT requis + vérification propriétaire
- **Paramètres optionnels** : title, content, image_base64
- **Statut** : ✅ Implémenté

#### BF4.7 : Supprimer son post
- **Description** : Effacer définitivement un post
- **Endpoint** : `DELETE /posts/{post_id}`
- **Authentification** : JWT requis + vérification propriétaire
- **Cascade** : Supprime commentaires, likes, shares associés
- **Statut** : ✅ Implémenté

---

### **BF5 - Analytics & Statistiques**

#### BF5.1 : Statistiques d'abonnements
- **Endpoint** : `GET /analytics/subscriptions`
- **Données** :
  - Total d'abonnements
  - Répartition par niveau (top: X, moyen: Y, bas: Z)
  - 5 abonnements récents avec dates
- **Statut** : ✅ Implémenté

#### BF5.2 : Statistiques de posts
- **Endpoint** : `GET /analytics/posts`
- **Données** :
  - Total de posts créés
  - Total likes reçus
  - Total commentaires reçus
  - Total partages
  - Post le plus liké
  - Timeline des posts (7 derniers jours)
- **Statut** : ✅ Implémenté

#### BF5.3 : Statistiques de notifications
- **Endpoint** : `GET /analytics/notifications`
- **Données** :
  - Total de notifications
  - Timeline des notifications (7 derniers jours)
  - 10 notifications récentes
- **Statut** : ✅ Implémenté

#### BF5.4 : Comparaisons et engagement
- **Endpoint** : `GET /analytics/comparison`
- **Données** :
  - Posts vs Subscriptions vs Notifications
  - Likes reçus vs Likes donnés
  - Taux d'engagement calculé
  - Score d'activité global
- **Statut** : ✅ Implémenté

#### BF5.5 : Vue d'ensemble
- **Endpoint** : `GET /analytics/overview`
- **Données** :
  - Âge du compte (jours)
  - Niveau d'activité (Débutant/Intermédiaire/Avancé/Expert)
  - Statistiques de contenu créé
  - Statistiques d'interactions
  - Statistiques reçues
- **Statut** : ✅ Implémenté

---

### **BF6 - Recherche & Exploration**

#### BF6.1 : Recherche de subreddits
- **Description** : Rechercher et valider un subreddit avant abonnement
- **Endpoint** : `GET /search?q=<subreddit_name>`
- **Validation Reddit** :
  1. Authentification Reddit via PRAW
  2. Vérification de l'existence du subreddit
  3. Gestion des erreurs (privé, inexistant)
- **Statut** : ✅ Implémenté

#### BF6.2 : Prévisualisation
- **Description** : Voir les 20 posts les plus populaires (hot)
- **Données** : titre, score, auteur, URL, timestamp
- **Calcul niveau** : Automatique selon le score
- **Statut** : ✅ Implémenté

#### BF6.3 : Validation en temps réel
- **Description** : Feedback immédiat sur la validité
- **Messages d'erreur** :
  - "Le subreddit 'xxx' n'existe pas ou est privé" (404)
  - "Erreur d'authentification Reddit" (500)
- **Statut** : ✅ Implémenté

#### BF6.4 : Autocomplétion
- **Description** : Suggestions de subreddits populaires
- **Statut** : ⚠️ Non implémenté (amélioration future)

---

## 📊 Résumé des Besoins Fonctionnels

| Catégorie | Total | Implémentés | En attente |
|-----------|-------|-------------|------------|
| **Gestion Utilisateurs** | 6 | 6 ✅ | 0 |
| **Abonnements Reddit** | 5 | 4 ✅ | 1 ⚠️ |
| **Notifications** | 5 | 5 ✅ | 0 |
| **Gestion Contenu** | 7 | 7 ✅ | 0 |
| **Analytics** | 5 | 5 ✅ | 0 |
| **Recherche** | 4 | 3 ✅ | 1 ⚠️ |
| **TOTAL** | **32** | **30 ✅** | **2 ⚠️** |

### Taux de complétion : **94%** ✅
