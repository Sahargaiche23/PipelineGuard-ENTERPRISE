# 📡 PipelineGuard Enterprise - Guide API

## 🔑 Authentification

Toutes les routes (sauf `/register` et `/login`) requièrent un **JWT Token**.

### **Header requis**
```http
Authorization: Bearer <jwt_token>
```

---

## 👤 Endpoints Authentification

### POST /register
**Description** : Créer un nouveau compte utilisateur

**Body** :
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response** : `200 OK`
```json
{
  "msg": "Registered"
}
```

---

### POST /login
**Description** : Se connecter et obtenir un token JWT

**Body** :
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response** : `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer"
}
```

---

### GET /profile
**Description** : Récupérer son profil utilisateur

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "bio": "Developer",
  "avatar_url": null,
  "avatar_base64": "data:image/png;base64,...",
  "created_at": "2025-11-01T10:00:00"
}
```

---

### PUT /profile
**Description** : Mettre à jour son profil

**Headers** : `Authorization: Bearer <token>`

**Body** (tous optionnels) :
```json
{
  "email": "newemail@example.com",
  "full_name": "John Doe",
  "bio": "Full Stack Developer",
  "avatar_base64": "data:image/png;base64,iVBORw0KGg..."
}
```

**Response** : `200 OK`
```json
{
  "message": "Profil mis à jour avec succès",
  "profile": { ... }
}
```

---

### DELETE /profile
**Description** : Supprimer définitivement son compte

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
{
  "message": "Compte supprimé avec succès"
}
```

---

## 🔍 Endpoints Reddit & Abonnements

### GET /search
**Description** : Rechercher un subreddit et voir les posts

**Headers** : `Authorization: Bearer <token>`

**Query Params** :
- `q` : Nom du subreddit (ex: "python")

**Exemple** : `/search?q=python`

**Response** : `200 OK`
```json
[
  {
    "id": "abc123",
    "title": "My first Python project",
    "level": "moyen",
    "url": "https://reddit.com/r/python/...",
    "author": "user123",
    "created_utc": 1699099200.0
  }
]
```

**Erreurs** :
- `400` : Subreddit name requis
- `404` : Subreddit inexistant ou privé
- `500` : Erreur authentification Reddit

---

### POST /subscribe
**Description** : S'abonner à un subreddit avec filtrage par niveau

**Headers** : `Authorization: Bearer <token>`

**Body** :
```json
{
  "topic": "python",
  "level": "top"
}
```

**Niveaux valides** : `"top"`, `"moyen"`, `"bas"`

**Response** : `200 OK`
```json
{
  "message": "Abonnement enregistré et notification créée"
}
```

**Erreurs** :
- `422` : Niveau invalide

---

### GET /my_posts
**Description** : Récupérer les posts Reddit filtrés par ses abonnements

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
[
  {
    "id": "def456",
    "title": "Advanced Python Tips",
    "level": "top",
    "url": "https://...",
    "author": "expert_dev",
    "created_utc": 1699099200.0,
    "topic": "python"
  }
]
```

---

## 🔔 Endpoints Notifications

### WS /ws/{token}
**Description** : WebSocket pour notifications temps réel

**Protocol** : WebSocket

**URL** : `ws://localhost:8000/ws/{jwt_token}`

**Messages reçus** :
```json
{
  "id": 42,
  "title": "Notification Reddit",
  "content": "Abonnement au topic 'angular' niveau 'top'",
  "url": "",
  "created_at": "2025-11-04T11:30:00"
}
```

---

### GET /notifications
**Description** : Historique des notifications

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
[
  {
    "id": 42,
    "title": "Notification Reddit",
    "content": "Abonnement au topic 'python' niveau 'top'",
    "url": "",
    "created_at": "2025-11-04T10:00:00"
  }
]
```

---

### DELETE /notifications
**Description** : Supprimer toutes les notifications

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
{
  "message": "5 notifications supprimées avec succès"
}
```

---

## 📊 Endpoints Analytics

### GET /analytics/subscriptions
**Description** : Statistiques des abonnements

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
{
  "total": 15,
  "by_level": {
    "top": 5,
    "moyen": 7,
    "bas": 3
  },
  "recent": [
    {
      "topic": "python",
      "level": "top",
      "created_at": "2025-11-04T10:00:00"
    }
  ]
}
```

---

### GET /analytics/posts
**Description** : Statistiques des posts créés

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
{
  "total_posts": 25,
  "total_likes": 150,
  "total_comments": 80,
  "total_shares": 30,
  "most_liked_post": {
    "id": 42,
    "title": "My Best Post",
    "likes": 75
  },
  "posts_last_7_days": [
    {"date": "2025-11-04", "count": 3}
  ]
}
```

---

### GET /analytics/notifications
**Description** : Statistiques des notifications

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
{
  "total": 100,
  "last_7_days": [
    {"date": "2025-11-04", "count": 10}
  ],
  "recent": [...]
}
```

---

### GET /analytics/comparison
**Description** : Comparaison des métriques

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
{
  "posts": 25,
  "subscriptions": 15,
  "notifications": 100,
  "likes_received": 150,
  "likes_given": 80,
  "engagement_rate": 6.0,
  "activity_score": 120
}
```

---

## 📝 Endpoints Posts

### POST /posts
**Description** : Créer un nouveau post

**Headers** : `Authorization: Bearer <token>`

**Body** :
```json
{
  "title": "My First Post",
  "content": "Hello World!",
  "image_base64": "data:image/png;base64,..." // optionnel
}
```

**Response** : `200 OK`
```json
{
  "id": 123,
  "message": "Post créé avec succès"
}
```

---

### GET /posts
**Description** : Fil d'actualités (tous les posts)

**Headers** : `Authorization: Bearer <token>`

**Query Params** (optionnels) :
- `skip` : Offset (défaut: 0)
- `limit` : Nombre de résultats (défaut: 50)

**Response** : `200 OK`
```json
[
  {
    "id": 123,
    "user_id": 1,
    "username": "johndoe",
    "avatar_base64": null,
    "title": "My Post",
    "content": "Content here",
    "image_base64": null,
    "likes_count": 10,
    "comments_count": 5,
    "shares_count": 2,
    "created_at": "2025-11-04T10:00:00",
    "updated_at": "2025-11-04T10:00:00",
    "is_liked": false
  }
]
```

---

### POST /posts/{post_id}/like
**Description** : Liker ou retirer son like d'un post

**Headers** : `Authorization: Bearer <token>`

**Response** : `200 OK`
```json
{
  "message": "Post liké",
  "liked": true
}
// OU
{
  "message": "Like retiré",
  "liked": false
}
```

---

### POST /posts/{post_id}/comments
**Description** : Ajouter un commentaire

**Headers** : `Authorization: Bearer <token>`

**Body** :
```json
{
  "content": "Great post!"
}
```

**Response** : `200 OK`
```json
{
  "id": 456,
  "message": "Commentaire ajouté avec succès"
}
```

---

## 🔧 Codes d'Erreur

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 400 | Bad Request (paramètre manquant/invalide) |
| 401 | Unauthorized (token invalide/expiré) |
| 403 | Forbidden (pas le propriétaire) |
| 404 | Not Found (ressource inexistante) |
| 422 | Unprocessable Entity (validation échouée) |
| 500 | Internal Server Error |

---

## 📚 Documentation Interactive

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
