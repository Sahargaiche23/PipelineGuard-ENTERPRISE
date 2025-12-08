# 📘 PipelineGuard Enterprise - Vue d'Ensemble

## 🎯 Présentation du Projet

**PipelineGuard Enterprise** est une **plateforme complète de surveillance et monitoring en temps réel** pour les données Reddit. C'est une application web moderne de type Enterprise qui combine microservices, streaming de données, et notifications temps réel.

### 🎓 Contexte
Projet développé dans le cadre d'un stage, représentant une solution enterprise-grade combinant plusieurs technologies modernes.

### 🔑 Fonctionnalités Principales
- ✅ S'abonner à des subreddits spécifiques
- ✅ Filtrer les posts par niveau d'importance (top, moyen, bas)
- ✅ Recevoir des notifications en temps réel via WebSocket
- ✅ Analyser ses abonnements et activités via dashboard
- ✅ Gérer son profil utilisateur avec avatar
- ✅ Créer et gérer des posts avec likes/commentaires
- ✅ Monitoring complet avec Prometheus & Grafana

### 📊 Métriques du Projet
- **14 endpoints** API REST
- **7 modèles** de données
- **9 composants** Angular
- **6 services** Docker
- **Tests E2E** avec Playwright

---

## 🛠️ Frameworks et Technologies

### **Backend Stack**
| Technologie | Version | Rôle |
|-------------|---------|------|
| **FastAPI** | 0.104.1 | Framework web Python moderne, rapide et asynchrone |
| **Uvicorn** | 0.24.0 | Serveur ASGI pour FastAPI |
| **SQLAlchemy** | 2.0.23 | ORM pour la gestion de base de données |
| **Pydantic** | 2.5.0 | Validation des données et sérialisation |
| **Passlib + Bcrypt** | 1.7.4 | Hachage sécurisé des mots de passe |
| **Python-Jose** | 3.3.0 | Création et validation de tokens JWT |
| **PRAW** | 7.7.1 | Reddit API Wrapper pour Python |
| **WebSockets** | 12.0 | Communication temps réel bidirectionnelle |

### **Frontend Stack**
| Technologie | Version | Rôle |
|-------------|---------|------|
| **Angular** | 16.2.0 | Framework SPA pour l'interface utilisateur |
| **TypeScript** | 5.1.3 | Langage typé pour JavaScript |
| **RxJS** | 7.8.0 | Programmation réactive et gestion des événements |
| **Angular Router** | 16.2.0 | Navigation entre les pages |
| **Angular Forms** | 16.2.12 | Gestion des formulaires réactifs |
| **Playwright** | 1.54.1 | Tests end-to-end automatisés |

### **Infrastructure & DevOps**
| Technologie | Rôle |
|-------------|------|
| **Docker** | Containerisation des services |
| **Docker Compose** | Orchestration multi-conteneurs |
| **PostgreSQL** | Base de données relationnelle production |
| **SQLite** | Base de données développement |
| **Redis** | Cache en mémoire |
| **Apache Kafka** | Message broker pour le streaming de données |
| **Zookeeper** | Coordination pour Kafka |
| **Nginx** | Serveur web et reverse proxy |
| **Prometheus** | Collecte de métriques |
| **Grafana** | Visualisation et dashboards |
| **Node Exporter** | Métriques système Linux |

---

## 🎯 Problématique

### **Contexte Métier**
Les entreprises et développeurs ont besoin de surveiller des flux d'informations Reddit en temps réel pour :
1. **Veille technologique** - Suivre les tendances et discussions importantes
2. **Support client** - Détecter les mentions de produits ou services
3. **Analyse de sentiment** - Comprendre l'opinion publique
4. **Détection d'opportunités** - Identifier les sujets populaires émergents

### **Défis Techniques Identifiés**
1. ❌ **Surcharge d'information** - Reddit génère des millions de posts quotidiens
2. ❌ **Pertinence des données** - Tous les posts n'ont pas la même valeur
3. ❌ **Délai de notification** - Besoin de notifications instantanées
4. ❌ **Scalabilité** - Gérer plusieurs utilisateurs et abonnements simultanés
5. ❌ **Sécurité** - Protéger les données utilisateurs et credentials Reddit

### **Limitations des Solutions Existantes**
- **Reddit natif** : Pas de filtres avancés par score, notifications limitées
- **IFTTT/Zapier** : Limité en fonctionnalités et coûteux pour usage intensif
- **Scripts custom** : Difficiles à maintenir, non scalables, pas d'interface

---

## ✅ Solutions Techniques Apportées

### **1. Architecture Microservices**
✅ **Séparation des responsabilités** - Backend/Frontend/Message Broker indépendants  
✅ **Scalabilité horizontale** - Chaque service peut être scalé individuellement  
✅ **Résilience** - Une panne d'un service n'affecte pas les autres  
✅ **Déploiement indépendant** - Mise à jour sans downtime

### **2. Filtrage Intelligent par Score**
✅ **Classification automatique** basée sur le score Reddit :
```python
- "top"   : score >= 1000  (posts viraux, haute visibilité)
- "moyen" : score >= 100   (discussions actives)
- "bas"   : score < 100    (posts récents, émergents)
```

### **3. Communication Temps Réel**
✅ **WebSocket bidirectionnel** - Notifications instantanées sans polling  
✅ **Architecture événementielle** - Kafka pour le streaming de données  
✅ **Persistance en DB** - Historique complet des notifications  
✅ **Reconnexion automatique** - Gestion des déconnexions réseau

### **4. Authentification & Sécurité**
✅ **JWT (JSON Web Tokens)** - Authentification stateless scalable  
✅ **Bcrypt avec salt** - Hachage sécurisé des mots de passe (12 rounds)  
✅ **CORS configuré** - Protection contre les attaques XSS/CSRF  
✅ **Validation Pydantic** - Toutes les entrées sont validées

### **5. Monitoring & Observabilité**
✅ **Prometheus** - Collecte de métriques applicatives et système  
✅ **Grafana** - Dashboards de visualisation temps réel  
✅ **Healthchecks** - Surveillance de la santé des services  
✅ **Logs structurés** - Traçabilité complète des opérations

### **6. Interface Utilisateur Moderne**
✅ **Angular SPA** - Application single-page fluide  
✅ **Responsive design** - Compatible mobile/tablette/desktop  
✅ **Feedback temps réel** - Messages de succès/erreur clairs  
✅ **Gestion d'état** - RxJS pour la réactivité

---

## 📐 Architecture Globale

```
┌────────────────────────────────────────────────────────┐
│                  CLIENT (Browser)                      │
│              Angular SPA (Port 4200)                   │
└────────────┬───────────────────────────────────────────┘
             │ HTTP/HTTPS + WebSocket
             ▼
┌────────────────────────────────────────────────────────┐
│               REVERSE PROXY (Nginx)                    │
│          Load Balancing + SSL/TLS (Port 80)           │
└────────────┬───────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐    ┌─────────────────────────────────────────┐
│ Static  │    │     BACKEND API (FastAPI - Port 8000)   │
│ Assets  │    │  ┌───────────────────────────────────┐  │
│ (CDN)   │    │  │  • Authentication (JWT)           │  │
└─────────┘    │  │  • Reddit Integration (PRAW)      │  │
               │  │  • WebSocket Manager              │  │
               │  │  • Business Logic                 │  │
               │  └───────────────────────────────────┘  │
               └────────┬────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ PostgreSQL  │  │    Redis    │  │    Kafka    │
│ (Port 5432) │  │ (Port 6379) │  │ (Port 9092) │
│   Database  │  │    Cache    │  │   Broker    │
└─────────────┘  └─────────────┘  └──────┬──────┘
                                          │
                                   ┌──────▼──────┐
                                   │  Zookeeper  │
                                   │ (Port 2181) │
                                   └─────────────┘

┌────────────────────────────────────────────────────────┐
│              MONITORING STACK                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐      │
│  │ Prometheus │◄─┤   Node     │  │  Grafana   │      │
│  │ (Port 9090)│  │  Exporter  │  │(Port 3000) │      │
│  │  Metrics   │  │ (Port 9100)│  │ Dashboards │      │
│  └────────────┘  └────────────┘  └────────────┘      │
└────────────────────────────────────────────────────────┘
```

### **Ports Utilisés**
- `4200` : Angular Development Server
- `8000` : FastAPI Backend API
- `80` : Nginx (Production Frontend)
- `5432` : PostgreSQL Database
- `6379` : Redis Cache
- `9092` : Kafka Broker
- `2181` : Zookeeper
- `9090` : Prometheus
- `3000` : Grafana
- `9100` : Node Exporter

---

## 🚀 Démarrage Rapide

### **Prérequis**
- Docker 20.10+ & Docker Compose 2.0+
- Node.js 18+ (développement frontend)
- Python 3.11+ (développement backend)

### **Lancement avec Docker**
```bash
# Cloner le repository
git clone https://github.com/Sahargaiche23/PipelineGuard-ENTERPRISE.git
cd PipelineGuard-ENTERPRISE

# Démarrer tous les services
docker-compose up -d

# Vérifier l'état des services
docker-compose ps
```

### **Développement Local**
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (nouveau terminal)
cd front/projet
npm install
ng serve
```

### **Accès aux Services**
- **Frontend** : http://localhost:4200
- **Backend API** : http://localhost:8000
- **Swagger Docs** : http://localhost:8000/docs
- **Grafana** : http://localhost:3000 (admin/admin123)
- **Prometheus** : http://localhost:9090
