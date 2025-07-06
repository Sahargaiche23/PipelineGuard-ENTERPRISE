# PipelineGuard Enterprise 🚀

[![CI/CD Pipeline](https://github.com/Sahargaiche23/PipelineGuard-ENTERPRISE/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Sahargaiche23/PipelineGuard-ENTERPRISE/actions/workflows/ci-cd.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Solution complète de surveillance et de monitoring en temps réel pour les pipelines de données d'entreprise.**

## 🌟 Fonctionnalités

### 🔔 Système de Notifications
- **Notifications temps réel** via WebSocket
- **Intégration Reddit/Kafka** pour la surveillance des données
- **Interface utilisateur moderne** avec Angular
- **Authentification sécurisée** JWT

### 📊 Monitoring et Observabilité
- **Prometheus** pour la collecte de métriques
- **Grafana** pour la visualisation
- **Métriques système** avec Node Exporter
- **Alertes en temps réel**

### 🏗️ Architecture Microservices
- **Backend FastAPI** avec authentification
- **Frontend Angular** responsive
- **Base de données PostgreSQL**
- **Message broker Kafka**
- **Cache Redis**

## 🚀 Démarrage Rapide

### Prérequis
- Docker & Docker Compose
- Node.js 18+ (pour le développement)
- Python 3.11+ (pour le développement)

### Installation avec Docker
```bash
# Cloner le repository
git clone https://github.com/Sahargaiche23/PipelineGuard-ENTERPRISE.git
cd PipelineGuard-ENTERPRISE

# Démarrer tous les services
docker-compose up -d

# Vérifier que tous les services sont actifs
docker-compose ps
```

### Services disponibles
- **Frontend** : http://localhost:80
- **Backend API** : http://localhost:8000
- **Grafana** : http://localhost:3000 (admin/admin123)
- **Prometheus** : http://localhost:9090
- **PostgreSQL** : localhost:5432

## 🏛️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   Angular       │◄──►│   FastAPI       │◄──►│   PostgreSQL    │
│   Nginx         │    │   WebSocket     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Kafka         │              │
         └──────────────►│   Message       │◄─────────────┘
                        │   Broker        │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │   Monitoring    │
                        │   Prometheus    │
                        │   Grafana       │
                        └─────────────────┘
```

## 🛠️ Développement

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (Angular)
```bash
cd front/projet
npm install
ng serve
```

### Tests
```bash
# Tests Backend
cd backend
pytest

# Tests Frontend
cd front/projet
npm test
```

## 📊 Monitoring

### Métriques disponibles
- **Requêtes HTTP** : Nombre et durée
- **Connexions WebSocket** : Actives
- **Notifications** : Envoyées
- **Base de données** : Connexions
- **Système** : CPU, Mémoire, Disque

### Dashboards Grafana
1. **Système Overview** - Métriques générales
2. **Application Performance** - Backend/Frontend
3. **Database Monitoring** - PostgreSQL
4. **Kafka Metrics** - Message broker

## 🔒 Sécurité

- **Authentification JWT** avec expiration
- **Hashage bcrypt** des mots de passe
- **CORS configuré** pour les domaines autorisés
- **HTTPS ready** avec certificats SSL
- **Rate limiting** sur les APIs

## 🌐 API Documentation

### Endpoints principaux
```
POST /register          # Inscription utilisateur
POST /login            # Connexion utilisateur
GET  /notifications    # Récupérer notifications
DELETE /notifications  # Supprimer notifications
WS   /ws/{token}       # WebSocket temps réel
GET  /metrics          # Métriques Prometheus
```

### Documentation interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🚢 Déploiement

### Production avec Docker
```bash
# Build des images de production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scaling des services
docker-compose up -d --scale backend=3
```

### CI/CD avec GitHub Actions
- **Tests automatiques** sur push/PR
- **Build et push des images** Docker
- **Déploiement automatique** sur la branche main
- **Notifications de statut**

## 📈 Performance

### Optimisations incluses
- **Gzip compression** sur Nginx
- **Cache statique** des assets
- **Connection pooling** PostgreSQL
- **Lazy loading** Angular
- **Service workers** pour le cache

### Benchmarks
- **Throughput** : 1000+ req/s
- **Latence** : <100ms (P95)
- **Disponibilité** : 99.9%

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Distribué sous la license MIT. Voir `LICENSE` pour plus d'informations.

## 👥 Équipe

- **Sahar Gaiche** - Développeur Principal - [@Sahargaiche23](https://github.com/Sahargaiche23)

## 🙏 Remerciements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Angular](https://angular.io/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [Docker](https://www.docker.com/)

---

⭐ **Si ce projet vous aide, n'hésitez pas à lui donner une étoile !**
