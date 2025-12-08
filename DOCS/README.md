# 📚 Documentation PipelineGuard Enterprise

Bienvenue dans la documentation complète du projet **PipelineGuard Enterprise**.

## 📖 Table des Matières

### [01 - Vue d'Ensemble](./01_VUE_ENSEMBLE.md)
- Présentation du projet
- Frameworks et technologies utilisés
- Problématique métier
- Solutions techniques apportées
- Architecture globale
- Démarrage rapide

### [02 - Besoins Fonctionnels](./02_BESOINS_FONCTIONNELS.md)
- BF1 : Gestion des utilisateurs (6 besoins)
- BF2 : Abonnements Reddit (5 besoins)
- BF3 : Système de notifications (5 besoins)
- BF4 : Gestion de contenu (7 besoins)
- BF5 : Analytics & statistiques (5 besoins)
- BF6 : Recherche & exploration (4 besoins)
- **Total : 32 besoins - 30 implémentés (94%)**

### [03 - Besoins Non-Fonctionnels](./03_BESOINS_NON_FONCTIONNELS.md)
- BNF1 : Performance (4 critères)
- BNF2 : Sécurité (6 critères)
- BNF3 : Disponibilité (4 critères)
- BNF4 : Scalabilité (4 critères)
- BNF5 : Maintenabilité (5 critères)
- BNF6 : Utilisabilité (4 critères)
- BNF7 : Compatibilité (3 critères)
- **Total : 30 critères - 25 conformes (83%)**

### [04 - Architecture Détaillée](./04_ARCHITECTURE_DETAILLEE.md)
- Architecture backend en couches
- Architecture frontend Angular
- Flux de données clés
- Modèle de données (7 tables)
- Architecture Docker
- Sécurité multi-couches
- Monitoring Prometheus/Grafana

### [05 - Guide API](./05_GUIDE_API.md)
- Endpoints authentification (5)
- Endpoints Reddit & abonnements (3)
- Endpoints notifications (3)
- Endpoints analytics (4)
- Endpoints posts (12+)
- Exemples de requêtes/réponses
- Codes d'erreur
- Documentation interactive (Swagger/ReDoc)

### [06 - Résumé Complet](./06_RESUME_COMPLET.md)
- Synthèse exécutive
- Stack technologique complète
- Problématique & solutions
- Récapitulatif besoins fonctionnels/non-fonctionnels
- Architecture simplifiée
- Modèle de données
- API endpoints (14 routes)
- Flux clés détaillés
- Déploiement Docker
- Développement local
- Métriques & monitoring
- Sécurité
- Prochaines étapes

---

## 🚀 Accès Rapide

### Pour les développeurs
→ **Commencer ici** : [01_VUE_ENSEMBLE.md](./01_VUE_ENSEMBLE.md)  
→ **API Reference** : [05_GUIDE_API.md](./05_GUIDE_API.md)  
→ **Architecture** : [04_ARCHITECTURE_DETAILLEE.md](./04_ARCHITECTURE_DETAILLEE.md)

### Pour les chefs de projet
→ **Vue d'ensemble** : [06_RESUME_COMPLET.md](./06_RESUME_COMPLET.md)  
→ **Besoins métier** : [02_BESOINS_FONCTIONNELS.md](./02_BESOINS_FONCTIONNELS.md)

### Pour les architectes
→ **Architecture** : [04_ARCHITECTURE_DETAILLEE.md](./04_ARCHITECTURE_DETAILLEE.md)  
→ **Performance** : [03_BESOINS_NON_FONCTIONNELS.md](./03_BESOINS_NON_FONCTIONNELS.md)

---

## 📊 Statistiques du Projet

| Métrique | Valeur |
|----------|--------|
| **Lignes de code** | ~5000+ |
| **Endpoints API** | 14 REST + 1 WebSocket |
| **Composants Angular** | 7 |
| **Services Docker** | 9 |
| **Tables DB** | 7 |
| **Besoins fonctionnels** | 30/32 (94%) ✅ |
| **Besoins non-fonctionnels** | 25/30 (83%) ✅ |
| **Tests E2E** | Playwright configuré ✅ |

---

## 🛠️ Technologies Principales

- **Backend** : FastAPI 0.104.1, Python 3.11+
- **Frontend** : Angular 16.2.0, TypeScript 5.1.3
- **Database** : PostgreSQL 15, SQLAlchemy 2.0.23
- **Streaming** : Apache Kafka, Zookeeper
- **Cache** : Redis 7
- **Monitoring** : Prometheus, Grafana
- **Infrastructure** : Docker, Docker Compose, Nginx

---

## 📞 Support

Pour toute question sur la documentation ou le projet :
- **GitHub** : [Sahargaiche23/PipelineGuard-ENTERPRISE](https://github.com/Sahargaiche23/PipelineGuard-ENTERPRISE)
- **Email** : Voir profil GitHub

---

**Dernière mise à jour** : Novembre 2025  
**Version** : 1.0.0
