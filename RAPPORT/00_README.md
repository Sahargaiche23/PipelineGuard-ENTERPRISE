# 📘 PipelineGuard Enterprise - Rapport de Projet

## 📋 Description

Ce dossier contient le **rapport complet du projet PipelineGuard Enterprise**, une plateforme de surveillance Reddit en temps réel développée dans le cadre d'un stage. Le rapport suit le plan classique d'un mémoire de projet informatique.

---

## 📚 Structure du Rapport

### [01 - Introduction](./01_INTRODUCTION.md)
- Contexte général du projet
- Problématique identifiée
- Objectifs du projet
- Méthodologie de développement
- Structure du rapport

### [02 - Étude du Projet](./02_ETUDE_PROJET.md)
- Analyse de l'existant
  - Reddit et son API
  - Solutions concurrentes
- Étude de faisabilité
  - Technique
  - Économique
  - Opérationnelle
- Choix technologiques justifiés
  - Stack Backend (FastAPI, PostgreSQL, PRAW)
  - Stack Frontend (Angular, TypeScript, RxJS)
  - Infrastructure (Docker, Kafka, Redis)

### [03 - Spécification des Besoins](./03_SPECIFICATION_BESOINS.md)
- **Besoins Fonctionnels** (28 besoins)
  - BF1 : Gestion des utilisateurs (6)
  - BF2 : Abonnements Reddit (5)
  - BF3 : Système de notifications (5)
  - BF4 : Gestion de contenu (7)
  - BF5 : Analytics et statistiques (5)
- **Besoins Non-Fonctionnels** (30 critères)
  - Performance
  - Sécurité
  - Disponibilité
  - Scalabilité
  - Maintenabilité
  - Utilisabilité
  - Compatibilité
- Récapitulatif : **100% besoins fonctionnels, 90% besoins non-fonctionnels**

### [04 - Conception](./04_CONCEPTION.md)
- Architecture globale (microservices)
- Architecture backend en couches
- Modèle de données relationnel
  - 7 tables (users, subscriptions, notifications, posts, comments, likes, shares)
  - Diagramme entité-relation
  - Cardinalités et contraintes
- Diagrammes de séquence
  - Authentification JWT
  - Abonnement à un subreddit
  - Notifications temps réel WebSocket
- Architecture frontend Angular
  - Structure modulaire
  - Services et composants
  - Routing avec guards
- Communication WebSocket

### [05 - Réalisation](./05_REALISATION.md)
- Environnement de développement
  - Outils et logiciels
  - Structure du projet
- Implémentation backend
  - Configuration FastAPI
  - Authentification JWT + Bcrypt
  - Intégration Reddit API (PRAW)
  - WebSocket temps réel
  - Analytics
- Implémentation frontend
  - AuthService
  - HTTP Interceptor JWT
  - WebSocket Service
  - Composants Angular
- Tests
  - Tests E2E (Playwright)
  - Tests API (Postman)
- Déploiement
  - Docker Compose
  - Commandes de déploiement
- Difficultés rencontrées et solutions
- Métriques du projet

### [06 - Conclusion et Perspectives](./06_CONCLUSION_PERSPECTIVES.md)
- Bilan du projet
  - Objectifs atteints (95%)
  - Indicateurs de réussite
  - Apports du projet
- Limites actuelles
  - Techniques
  - Fonctionnelles
  - Opérationnelles
- Perspectives d'évolution
  - Court terme (sécurité, tests, fonctionnalités)
  - Moyen terme (performance, UX, IA)
  - Long terme (monétisation, nouvelles plateformes, cloud)
- Impact et valeur ajoutée
- Conclusion générale
- Remerciements
- Références

---

## 🎯 Résumé Exécutif

**PipelineGuard Enterprise** est une plateforme web moderne permettant la **surveillance Reddit en temps réel** avec :
- ✅ **Filtrage intelligent** par score (top/moyen/bas)
- ✅ **Notifications instantanées** via WebSocket
- ✅ **Interface Angular** responsive
- ✅ **Authentification JWT** sécurisée
- ✅ **Analytics complets** avec dashboard
- ✅ **Architecture microservices** scalable (Docker)

### Chiffres Clés
- **28 besoins fonctionnels** implémentés (100%)
- **27/30 besoins non-fonctionnels** conformes (90%)
- **14 endpoints REST** + 1 WebSocket
- **7 tables** de base de données
- **9 services** Docker orchestrés
- **< 150ms** temps de réponse API moyen
- **< 100ms** latence WebSocket
- **2 mois** de développement

---

## 🛠️ Technologies Utilisées

### Backend
- **FastAPI 0.104.1** - Framework web Python async
- **SQLAlchemy 2.0.23** - ORM
- **PostgreSQL 15** - Base de données
- **PRAW 7.7.1** - Reddit API Wrapper
- **JWT + Bcrypt** - Authentification sécurisée
- **WebSockets 12.0** - Temps réel

### Frontend
- **Angular 16.2.0** - Framework SPA
- **TypeScript 5.1.3** - Langage typé
- **RxJS 7.8.0** - Programmation réactive
- **Playwright 1.54.1** - Tests E2E

### Infrastructure
- **Docker** - Containerisation
- **Docker Compose** - Orchestration
- **Apache Kafka** - Message broker
- **Redis 7** - Cache
- **Nginx** - Reverse proxy
- **Zookeeper** - Coordination Kafka

---

## 📊 Schéma d'Architecture

```
┌──────────────┐
│   Angular    │  Frontend SPA (Port 4200)
│   Browser    │
└──────┬───────┘
       │ HTTP/HTTPS + WebSocket
       ▼
┌──────────────┐
│    Nginx     │  Reverse Proxy (Port 80)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   FastAPI    │  Backend API (Port 8000)
└──────┬───────┘
       │
   ┌───┴────┬──────────┬────────┐
   │        │          │        │
   ▼        ▼          ▼        ▼
┌─────┐ ┌──────┐ ┌────────┐ ┌──────┐
│PgSQL│ │Redis │ │ Kafka  │ │ WS   │
└─────┘ └──────┘ └───┬────┘ └──────┘
                     │
                     ▼
               ┌──────────┐
               │Zookeeper │
               └──────────┘
```

---

## 📖 Comment Utiliser ce Rapport

### Pour une lecture complète
Lire dans l'ordre : **01 → 02 → 03 → 04 → 05 → 06**

### Pour une vue d'ensemble rapide
Lire : **01_INTRODUCTION** + **06_CONCLUSION_PERSPECTIVES**

### Pour les aspects techniques
Lire : **04_CONCEPTION** + **05_REALISATION**

### Pour comprendre les besoins
Lire : **03_SPECIFICATION_BESOINS**

### Pour le contexte et choix
Lire : **02_ETUDE_PROJET**

---

## 👤 Auteur

**Sahar Gaiche**
- GitHub : [@Sahargaiche23](https://github.com/Sahargaiche23)
- Repository : [PipelineGuard-ENTERPRISE](https://github.com/Sahargaiche23/PipelineGuard-ENTERPRISE)
- License : MIT

---

## 📅 Informations Projet

- **Date de début** : Août 2025
- **Date de fin** : Novembre 2025
- **Durée** : 2 mois
- **Contexte** : Projet de stage
- **Version** : 1.0.0
- **Statut** : ✅ Production ready

---

## 🔗 Liens Utiles

- **Documentation API** : http://localhost:8000/docs (Swagger)
- **Application** : http://localhost:4200
- **Repository GitHub** : https://github.com/Sahargaiche23/PipelineGuard-ENTERPRISE
- **Documentation Technique** : Dossier `/DOCS`

---

## 📝 Notes

Ce rapport a été rédigé **sans inclure Prometheus et Grafana** comme demandé. L'accent est mis sur :
- ✅ L'architecture microservices
- ✅ L'intégration Reddit API
- ✅ Le système de notifications WebSocket
- ✅ L'authentification JWT
- ✅ Les analytics applicatifs

Pour la documentation incluant le monitoring complet, consulter le dossier `/DOCS`.

---

**Dernière mise à jour** : Novembre 2025
