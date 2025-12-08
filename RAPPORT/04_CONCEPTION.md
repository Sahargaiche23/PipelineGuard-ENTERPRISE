# 4. Conception

## 4.1 Diagramme de Cas d'Utilisation Général

### 4.1.1 Vue d'Ensemble

Le diagramme de cas d'utilisation suivant présente les interactions entre les acteurs et le système PipelineGuard Enterprise.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PIPELINEGUARD ENTERPRISE                         │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              GESTION DES UTILISATEURS                        │ │
│  │  ┌─────────────────┐      ┌──────────────────┐             │ │
│  │  │   S'inscrire    │      │  Se connecter    │             │ │
│  │  └─────────────────┘      └──────────────────┘             │ │
│  │  ┌─────────────────┐      ┌──────────────────┐             │ │
│  │  │ Consulter profil│      │ Modifier profil  │             │ │
│  │  └─────────────────┘      └──────────────────┘             │ │
│  │  ┌─────────────────┐                                        │ │
│  │  │ Uploader avatar │                                        │ │
│  │  └─────────────────┘                                        │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │          ABONNEMENTS REDDIT                                  │ │
│  │  ┌─────────────────────┐    ┌────────────────────┐         │ │
│  │  │ Rechercher          │    │ Prévisualiser      │         │ │
│  │  │ subreddit           │───►│ posts              │         │ │
│  │  └─────────────────────┘    └────────────────────┘         │ │
│  │                                       │                      │ │
│  │                                       ▼                      │ │
│  │  ┌───────────────────────────────────────────────┐         │ │
│  │  │ S'abonner avec niveau (top/moyen/bas)        │         │ │
│  │  └───────────────────────────────────────────────┘         │ │
│  │                      │                                       │ │
│  │                      │ «include»                            │ │
│  │                      ▼                                       │ │
│  │  ┌───────────────────────────────────────────────┐         │ │
│  │  │ Valider existence subreddit                  │◄────────┼─┼─── API Reddit
│  │  └───────────────────────────────────────────────┘         │ │
│  │                                                              │ │
│  │  ┌─────────────────────┐                                   │ │
│  │  │ Consulter mes posts │                                   │ │
│  │  │ filtrés             │                                   │ │
│  │  └─────────────────────┘                                   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │             NOTIFICATIONS TEMPS RÉEL                         │ │
│  │  ┌─────────────────────┐    ┌────────────────────┐         │ │
│  │  │ Se connecter via    │    │ Recevoir           │         │ │
│  │  │ WebSocket           │───►│ notifications      │         │ │
│  │  └─────────────────────┘    └────────────────────┘         │ │
│  │                                                              │ │
│  │  ┌─────────────────────┐    ┌────────────────────┐         │ │
│  │  │ Consulter historique│    │ Supprimer toutes   │         │ │
│  │  │ notifications       │    │ notifications      │         │ │
│  │  └─────────────────────┘    └────────────────────┘         │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │             GESTION DE CONTENU                               │ │
│  │  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐ │ │
│  │  │ Créer post      │  │ Modifier     │  │ Supprimer      │ │ │
│  │  │                 │  │ post         │  │ post           │ │ │
│  │  └─────────────────┘  └──────────────┘  └────────────────┘ │ │
│  │                                                              │ │
│  │  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐ │ │
│  │  │ Liker post      │  │ Commenter    │  │ Partager       │ │ │
│  │  │                 │  │ post         │  │ post           │ │ │
│  │  └─────────────────┘  └──────────────┘  └────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              ANALYTICS ET STATISTIQUES                       │ │
│  │  ┌─────────────────────────┐  ┌──────────────────────────┐ │ │
│  │  │ Consulter stats         │  │ Consulter stats          │ │ │
│  │  │ abonnements             │  │ posts                    │ │ │
│  │  └─────────────────────────┘  └──────────────────────────┘ │ │
│  │                                                              │ │
│  │  ┌─────────────────────────┐  ┌──────────────────────────┐ │ │
│  │  │ Consulter stats         │  │ Vue comparaison          │ │ │
│  │  │ notifications           │  │ globale                  │ │ │
│  │  └─────────────────────────┘  └──────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌──────────┐                                                  ┌──────────────┐
│Utilisateur│                                                  │  API Reddit  │
│          │                                                  │   (PRAW)     │
└──────────┘                                                  └──────────────┘
```

### 4.1.2 Acteurs du Système

| Acteur | Description | Responsabilités |
|--------|-------------|-----------------|
| **Utilisateur** | Personne utilisant la plateforme | - Créer un compte<br>- Gérer ses abonnements<br>- Consulter posts et notifications<br>- Interagir avec le contenu (like, comment) |
| **API Reddit (PRAW)** | Système externe | - Fournir les données des subreddits<br>- Valider l'existence des subreddits<br>- Fournir les posts avec métadonnées |
| **Système (Backend)** | PipelineGuard Backend | - Authentifier les utilisateurs<br>- Gérer la persistance des données<br>- Envoyer notifications temps réel<br>- Calculer les analytics |

### 4.1.3 Principaux Cas d'Utilisation

#### Cas d'Utilisation Prioritaires (Must Have)

| ID | Cas d'Utilisation | Description | Acteur Principal |
|----|-------------------|-------------|------------------|
| **UC-01** | S'inscrire | Créer un nouveau compte utilisateur | Utilisateur |
| **UC-02** | Se connecter | Authentification avec JWT | Utilisateur |
| **UC-03** | Rechercher subreddit | Rechercher et prévisualiser un subreddit | Utilisateur |
| **UC-04** | S'abonner avec niveau | Créer abonnement avec filtrage (top/moyen/bas) | Utilisateur |
| **UC-05** | Consulter posts filtrés | Voir posts selon abonnements | Utilisateur |
| **UC-06** | Recevoir notifications | Notifications temps réel via WebSocket | Utilisateur |

#### Cas d'Utilisation Secondaires (Should Have)

| ID | Cas d'Utilisation | Description | Acteur Principal |
|----|-------------------|-------------|------------------|
| **UC-07** | Modifier profil | Mettre à jour email, nom, bio, avatar | Utilisateur |
| **UC-08** | Consulter analytics | Voir statistiques abonnements/posts/notifications | Utilisateur |
| **UC-09** | Créer post | Publier un nouveau post | Utilisateur |
| **UC-10** | Liker/Commenter | Interagir avec posts | Utilisateur |

#### Relations entre Cas d'Utilisation

**Relations «include»** (obligatoires) :
- **S'abonner** `include` **Valider existence subreddit** : Toujours vérifier avant abonnement
- **Se connecter** `include` **Valider JWT** : Authentification systématique
- **Rechercher subreddit** `include` **Appeler API Reddit** : Récupération données

**Relations «extend»** (optionnelles) :
- **Modifier profil** `extend` **Uploader avatar** : Optionnel lors modification
- **Consulter posts** `extend` **Filtrer par niveau** : Filtrage optionnel

## 4.2 Architecture Globale

### 4.2.1 Patron Architectural : Microservices

Le projet adopte une **architecture microservices** pour garantir modularité, scalabilité et maintenabilité.

```
┌──────────────────┐
│  Client Browser  │  Angular SPA (Port 4200)
└────────┬─────────┘
         │ HTTP/HTTPS + WebSocket
         ▼
┌────────────────────┐
│   Reverse Proxy    │  Nginx (Port 80)
│  Load Balancer     │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│   Backend API      │  FastAPI (Port 8000)
│   + WebSocket      │  - REST endpoints
└────────┬───────────┘  - WebSocket Manager
         │
    ┌────┴───────────────┬──────────┐
    │                    │          │
    ▼                    ▼          ▼
┌─────────┐      ┌──────────┐  ┌────────┐
│Postgre  │      │  Redis   │  │ Kafka  │
│SQL DB   │      │  Cache   │  │ Broker │
└─────────┘      └──────────┘  └───┬────┘
                                    │
                             ┌──────▼──────┐
                             │  Zookeeper  │
                             └─────────────┘
```

**Avantages de l'architecture** :
- ✅ **Séparation des responsabilités** : Chaque service a un rôle précis
- ✅ **Scalabilité indépendante** : Scale backend sans toucher DB
- ✅ **Résilience** : Panne d'un service n'affecte pas les autres
- ✅ **Déploiement continu** : Mise à jour sans downtime complet
- ✅ **Technologie hétérogène** : Chaque service peut utiliser son stack optimal

### 4.2.2 Architecture Backend en Couches

```
┌─────────────────────────────────────────┐
│     PRESENTATION LAYER                  │
│  ┌──────────────────────────────────┐   │
│  │ FastAPI Routes                   │   │
│  │ - main.py, auth.py, posts.py     │   │
│  │ - Validation Pydantic            │   │
│  │ - Sérialisation JSON             │   │
│  │ - Gestion exceptions HTTP        │   │
│  └──────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     AUTHENTICATION LAYER                │
│  ┌──────────────────────────────────┐   │
│  │ JWT Middleware                   │   │
│  │ - Token validation               │   │
│  │ - Signature verification         │   │
│  │ - User extraction                │   │
│  │ - get_current_user() dependency  │   │
│  └──────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     BUSINESS LOGIC LAYER                │
│  ┌──────────────────────────────────┐   │
│  │ Services:                        │   │
│  │ - UserService                    │   │
│  │ - RedditIntegrationService       │   │
│  │ - SubscriptionService            │   │
│  │ - PostService                    │   │
│  │ - AnalyticsService               │   │
│  │ - WebSocketManager               │   │
│  └──────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     DATA ACCESS LAYER                   │
│  ┌──────────────────────────────────┐   │
│  │ SQLAlchemy ORM                   │   │
│  │ - Models (7 tables)              │   │
│  │ - Session Management             │   │
│  │ - Connection Pooling             │   │
│  │ - Query Builder                  │   │
│  └──────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
        ┌──────▼──────┐
        │ PostgreSQL  │
        │  Database   │
        └─────────────┘
```

**Séparation des responsabilités** :
- **Presentation** : Communication HTTP/WebSocket
- **Authentication** : Sécurité et identification
- **Business Logic** : Règles métier et orchestration
- **Data Access** : Persistance et requêtes

## 4.3 Modèle de Données

### 4.3.1 Schéma Relationnel

```sql
┌─────────────────────┐
│      users          │
├─────────────────────┤
│ PK  id              │
│ UK  username        │
│     hashed_password │
│ UK  email           │
│     full_name       │
│     bio             │
│     avatar_base64   │
│     created_at      │
└──────┬──────────────┘
       │ 1
       │
       │ N
       ├────────────────────┐
       │                    │
┌──────▼────────┐   ┌───────▼────────┐
│subscriptions  │   │ notifications  │
├───────────────┤   ├────────────────┤
│ PK id         │   │ PK id          │
│ FK user_id    │   │ FK user_id     │
│    topic      │   │    content     │
│    level      │   │    created_at  │
│    created_at │   │ UK(user,content)
└───────────────┘   └────────────────┘

       │ N
┌──────▼──────────┐
│     posts       │
├─────────────────┤
│ PK id           │
│ FK user_id      │
│    title        │
│    content      │
│    image_base64 │
│    likes_count  │
│    comments_count
│    shares_count │
│    created_at   │
│    updated_at   │
└──────┬──────────┘
       │ 1
       ├──────────────┬───────────────┐
       │ N            │ N             │ N
┌──────▼────┐  ┌──────▼─────┐  ┌──────▼────┐
│ comments  │  │   likes    │  │  shares   │
├───────────┤  ├────────────┤  ├───────────┤
│PK id      │  │PK id       │  │PK id      │
│FK post_id │  │FK post_id  │  │FK post_id │
│FK user_id │  │FK user_id  │  │FK user_id │
│  content  │  │created_at  │  │shared_to_profile
│created_at │  │UK(post,user)  │created_at │
└───────────┘  └────────────┘  └───────────┘
```

### 4.3.2 Description des Tables

#### Table `users`
- **Rôle** : Stockage des comptes utilisateurs
- **Clé primaire** : `id` (INTEGER AUTO_INCREMENT)
- **Contraintes** : 
  - `username` UNIQUE
  - `email` UNIQUE (nullable)
- **Sécurité** : `hashed_password` (Bcrypt 12 rounds)

#### Table `subscriptions`
- **Rôle** : Abonnements Reddit des utilisateurs
- **Clé étrangère** : `user_id` → users(id)
- **Champs métier** :
  - `topic` : Nom du subreddit (ex: "python")
  - `level` : Niveau de filtrage ("top", "moyen", "bas")

#### Table `notifications`
- **Rôle** : Historique des notifications
- **Contrainte UNIQUE** : `(user_id, content)` pour éviter doublons
- **Index** : Sur `user_id` et `created_at` pour performance

#### Table `posts`
- **Rôle** : Publications des utilisateurs
- **Compteurs** : `likes_count`, `comments_count`, `shares_count` (dénormalisation pour performance)
- **Cascade** : Suppression post → cascade sur comments/likes/shares

#### Tables `comments`, `likes`, `shares`
- **Rôle** : Interactions sociales
- **Contrainte likes** : UNIQUE(post_id, user_id) - un utilisateur ne peut liker qu'une fois

### 4.3.3 Cardinalités

| Relation | Type | Description |
|----------|------|-------------|
| User → Subscription | 1:N | Un utilisateur a plusieurs abonnements |
| User → Notification | 1:N | Un utilisateur reçoit plusieurs notifications |
| User → Post | 1:N | Un utilisateur crée plusieurs posts |
| Post → Comment | 1:N | Un post a plusieurs commentaires |
| Post → Like | 1:N | Un post peut être liké par plusieurs users |
| Post → Share | 1:N | Un post peut être partagé plusieurs fois |

## 4.4 Diagrammes de Séquence

### 4.4.1 Cas d'usage : Connexion et Authentification JWT

```
Acteur: Utilisateur
Client: Angular
Backend: FastAPI
Database: PostgreSQL

┌─────────┐   ┌────────┐   ┌─────────┐   ┌──────────┐
│Utilisateur  │ Client │   │ Backend │   │ Database │
└────┬────┘   └───┬────┘   └────┬────┘   └────┬─────┘
     │            │              │             │
     │ 1. Saisit identifiants   │             │
     ├───────────►│              │             │
     │            │              │             │
     │            │ 2. POST /login            │
     │            │ {username, password}      │
     │            ├─────────────►│             │
     │            │              │             │
     │            │              │ 3. Query User
     │            │              ├────────────►│
     │            │              │             │
     │            │              │◄────────────┤
     │            │              │ User object │
     │            │              │             │
     │            │              │ 4. Verify   │
     │            │              │ Bcrypt hash │
     │            │              │             │
     │            │              │ 5. Generate │
     │            │              │ JWT token   │
     │            │              │ (exp 30min) │
     │            │              │             │
     │            │◄─────────────┤             │
     │            │ 6. {access_token}         │
     │            │                            │
     │◄───────────┤                            │
     │ 7. Token stocké (localStorage)         │
     │            │                            │
     │ 8. Navigation vers dashboard           │
     ├───────────►│                            │
     │            │ 9. GET /profile           │
     │            │ Header: Bearer {token}    │
     │            ├─────────────►│             │
     │            │              │ 10. Validate│
     │            │              │ JWT token   │
     │            │              │             │
     │            │              │ 11. Extract │
     │            │              │ username    │
     │            │              │             │
     │            │              │ 12. Query   │
     │            │              ├────────────►│
     │            │              │             │
     │            │              │◄────────────┤
     │            │              │ User profile│
     │            │◄─────────────┤             │
     │            │ 13. {profile}             │
     │◄───────────┤                            │
     │ 14. Affichage profil                   │
```

**Étapes clés** :
1. Utilisateur saisit credentials
2. Client envoie POST /login
3. Backend vérifie username en DB
4. Backend vérifie password avec Bcrypt
5. Backend génère JWT (payload: {sub: username, exp: timestamp})
6. Client reçoit token et le stocke
7-14. Requêtes suivantes utilisent Header Authorization: Bearer {token}

### 4.4.2 Cas d'usage : Abonnement à un Subreddit

```
┌──────────┐  ┌────────┐  ┌─────────┐  ┌──────────┐  ┌────────┐
│Utilisateur  │ Client │  │ Backend │  │ Database │  │ Reddit │
└─────┬────┘  └───┬────┘  └────┬────┘  └────┬─────┘  └───┬────┘
      │           │             │            │            │
      │ 1. Saisit "python"      │            │            │
      ├──────────►│             │            │            │
      │           │ 2. GET /search?q=python  │            │
      │           ├────────────►│            │            │
      │           │             │ 3. PRAW    │            │
      │           │             │ subreddit()│            │
      │           │             ├───────────────────────►│
      │           │             │            │            │
      │           │             │◄───────────────────────┤
      │           │             │ Hot posts (20)         │
      │           │◄────────────┤            │            │
      │           │ 4. Liste posts           │            │
      │◄──────────┤                          │            │
      │ 5. Affiche preview                   │            │
      │           │                          │            │
      │ 6. Clique "S'abonner - Top"         │            │
      ├──────────►│                          │            │
      │           │ 7. POST /subscribe       │            │
      │           │ {topic:"python",         │            │
      │           │  level:"top"}            │            │
      │           ├────────────►│            │            │
      │           │             │ 8. Validate│            │
      │           │             │ level      │            │
      │           │             │            │            │
      │           │             │ 9. Check   │            │
      │           │             │ duplicate  │            │
      │           │             ├───────────►│            │
      │           │             │            │            │
      │           │             │◄───────────┤            │
      │           │             │ None       │            │
      │           │             │            │            │
      │           │             │ 10. INSERT │            │
      │           │             │ Subscription            │
      │           │             ├───────────►│            │
      │           │             │            │            │
      │           │             │ 11. INSERT │            │
      │           │             │ Notification            │
      │           │             ├───────────►│            │
      │           │             │            │            │
      │           │             │ 12. COMMIT │            │
      │           │             ├───────────►│            │
      │           │◄────────────┤            │            │
      │           │ 13. {message: OK}        │            │
      │◄──────────┤                          │            │
      │ 14. Confirmation                     │            │
      │           │                          │            │
      │ 15. WebSocket push notification      │            │
      │◄──────────┤                          │            │
```

**Étapes importantes** :
- Étapes 2-5 : Prévisualisation avant abonnement
- Étape 8 : Validation niveau (sécurité côté serveur)
- Étape 9 : Prévention doublons
- Étapes 10-12 : Transaction atomique (subscription + notification)
- Étape 15 : Notification temps réel via WebSocket

## 4.5 Architecture Frontend Angular

### 4.5.1 Structure Modulaire

```
src/app/
├── app.module.ts (module racine)
├── app-routing.module.ts
├── app.component.ts
│
├── components/
│   ├── login/
│   │   ├── login.component.ts
│   │   ├── login.component.html
│   │   └── login.component.css
│   │
│   ├── register/
│   ├── profile/
│   ├── subscribe/
│   ├── my-posts/
│   ├── analytics/
│   └── notifications/
│
├── services/
│   ├── auth.service.ts
│   ├── http.service.ts
│   └── websocket.service.ts
│
└── guards/
    └── auth.guard.ts
```

### 4.5.2 Services Angular

**AuthService** : Gestion authentification
```typescript
login(username, password) → Observable<{access_token}>
logout() → void
isAuthenticated() → boolean
getToken() → string | null
```

**HttpService** : Communication API
```typescript
get(url) → Observable<T>
post(url, body) → Observable<T>
put(url, body) → Observable<T>
delete(url) → Observable<T>
// Interceptor JWT automatique
```

**WebSocketService** : Notifications temps réel
```typescript
connect(token) → void
notifications$ → Observable<Notification>
disconnect() → void
```

### 4.5.3 Routing

```typescript
const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { 
    path: 'profile', 
    component: ProfileComponent,
    canActivate: [AuthGuard]
  },
  { 
    path: 'subscribe', 
    component: SubscribeComponent,
    canActivate: [AuthGuard]
  },
  // ... autres routes protégées
];
```

**AuthGuard** : Protège les routes privées, redirige vers /login si non authentifié.

## 4.6 Communication WebSocket

### Architecture WebSocket Manager

```
Backend:
┌──────────────────────────────────────┐
│      WebSocket Manager               │
├──────────────────────────────────────┤
│  connections: Map<username, WebSocket>
│                                      │
│  connect(username, ws)               │
│  disconnect(username)                │
│  send_to_user(username, message)    │
│                                      │
│  async polling_loop():               │
│    while True:                       │
│      await asyncio.sleep(5)          │
│      for user in connections:        │
│        new_notifs = query_new(user)  │
│        if new_notifs:                │
│          send_to_user(user, notifs)  │
└──────────────────────────────────────┘
```

**Stratégie** : Polling toutes les 5 secondes pour vérifier les nouvelles notifications, puis push via WebSocket.

**Avantages** :
- ✅ Simple à implémenter
- ✅ Latence acceptable (< 5s)
- ✅ Charge DB maîtrisée

**Alternative future** : Event-driven avec Kafka Consumer → WebSocket direct (latence < 100ms).
