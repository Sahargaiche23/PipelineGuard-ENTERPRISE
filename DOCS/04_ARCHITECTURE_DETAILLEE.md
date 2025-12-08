# 🏗️ PipelineGuard Enterprise - Architecture Détaillée

## 🔄 Architecture Backend en Couches

### **Presentation Layer - API Endpoints**

**Fichier** : `main.py`, `auth.py`, `posts.py`, `analytics.py`

- **14 endpoints REST** + 1 WebSocket
- **Validation automatique** avec Pydantic
- **Documentation auto** : Swagger/ReDoc
- **CORS** : Configuration pour localhost:4200

### **Authentication Layer**

```python
JWT Flow:
1. POST /login → Verify Bcrypt → Generate JWT (HS256, 30min)
2. Requests → Header: Authorization: Bearer <token>
3. Middleware → Validate → Extract user → Inject in context

get_current_user(credentials) → User or 401
```

### **Business Logic Layer**

| Service | Responsabilité |
|---------|----------------|
| **User Management** | Registration, Login, Profile CRUD, Avatar upload |
| **Reddit Integration** | PRAW client, Subreddit validation, Hot posts retrieval |
| **Subscription** | Create/Filter subscriptions, Level validation |
| **Post Management** | CRUD, Like/Comment/Share, Owner verification |
| **Analytics** | Aggregations, Metrics, Timeline (7 days) |
| **WebSocket Manager** | Connection registry, Notifications polling (5s) |

### **Data Access Layer**

**SQLAlchemy ORM** avec 7 modèles :
- `User`, `Subscription`, `Notification`, `Post`, `Comment`, `Like`, `Share`, `RedditPost`
- Connection pooling configuré
- Session management avec context manager

---

## 🖥️ Architecture Frontend Angular

### **Structure des Composants**

```
app/
├── components/
│   ├── login/
│   ├── register/
│   ├── profile/
│   ├── subscribe/
│   ├── my-posts/
│   ├── analytics/
│   └── notifications/
├── services/
│   ├── auth.service.ts        (JWT storage, guards)
│   ├── http.service.ts        (API calls)
│   └── websocket.service.ts   (Real-time)
└── guards/
    └── auth.guard.ts          (Route protection)
```

### **Services Angular**

- **AuthService** : Login/Logout, Token storage (localStorage), isAuthenticated()
- **HttpService** : HTTP requests avec intercepteur JWT
- **WebSocketService** : Connexion WS, RxJS Observable pour notifications

---

## 🔀 Flux de Données Clés

### **1. Flux d'Abonnement**

```
User → Subscribe Component → POST /subscribe {topic, level}
  → Backend validate level → Insert Subscription
  → Create Notification → Commit DB
  → WebSocket push notification → UI update
```

### **2. Flux WebSocket Notifications**

```
Connect: WS /ws/{jwt}
  → Validate JWT → Query existing notifications → Send all
  → Start async loop (5s):
    - Query new notifications
    - Send via WebSocket
    - Frontend RxJS Observable updates UI
```

### **3. Flux d'Authentification**

```
Login → POST /login → Verify password
  → Generate JWT → Return token
  → Frontend store in localStorage
  → All requests: Header Authorization: Bearer <token>
  → Backend Dependency: get_current_user() validates
```

---

## 📊 Modèle de Données

### **Relations**

```
User 1─────N Subscription
User 1─────N Notification
User 1─────N Post
Post 1─────N Comment
Post 1─────N Like (UNIQUE post_id, user_id)
Post 1─────N Share
```

### **Tables Principales**

| Table | Clé Primaire | Indexes | Contraintes |
|-------|--------------|---------|-------------|
| users | id | username | UNIQUE username, email |
| subscriptions | id | user_id | - |
| notifications | id | user_id | UNIQUE(user_id, content) |
| posts | id | user_id | - |
| comments | id | post_id, user_id | FK post, user |
| likes | id | post_id, user_id | UNIQUE(post_id, user_id) |

---

## 🐳 Architecture Docker

### **Services Docker Compose**

```yaml
services:
  postgres:     # Database (Port 5432)
  redis:        # Cache (Port 6379)
  zookeeper:    # Kafka coordinator (Port 2181)
  kafka:        # Message broker (Port 9092)
  backend:      # FastAPI (Port 8000)
  frontend:     # Angular + Nginx (Port 80)
  prometheus:   # Metrics (Port 9090)
  grafana:      # Dashboards (Port 3000)
  node-exporter: # System metrics (Port 9100)
```

### **Réseau**
- **Bridge network** : `pipelineguard_network`
- **Volumes persistants** : postgres_data, redis_data, prometheus_data, grafana_data

---

## 🔒 Sécurité

### **Couche 1 - Transport**
- CORS : Whitelist localhost:4200
- HTTPS ready : Nginx SSL termination

### **Couche 2 - Authentification**
- JWT : HS256, expiration 30min
- Bcrypt : 12 rounds pour passwords

### **Couche 3 - Autorisation**
- Dependency injection : `get_current_user()`
- Owner verification : Edit/Delete posts

### **Couche 4 - Données**
- SQLAlchemy ORM : Protection SQL injection
- Pydantic : Validation des entrées

---

## 📈 Monitoring

### **Métriques Prometheus**
- HTTP requests count/latency
- WebSocket connections actives
- Database connection pool
- System metrics (CPU, RAM, Disk)

### **Dashboards Grafana**
- Application Performance
- Database Monitoring
- Kafka Metrics
- System Overview
