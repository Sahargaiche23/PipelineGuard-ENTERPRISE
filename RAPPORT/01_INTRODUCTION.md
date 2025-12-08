# 1. Introduction

## 1.1 Contexte Général

Dans un monde numérique en constante évolution, les réseaux sociaux génèrent quotidiennement des millions d'informations. **Reddit**, l'une des plus grandes plateformes de discussion au monde, héberge plus de 500 millions d'utilisateurs actifs et des milliers de communautés (subreddits) couvrant tous les domaines : technologie, science, business, divertissement, etc.

Les entreprises, développeurs et professionnels ont besoin de **surveiller ces flux d'informations** pour :
- Effectuer une **veille technologique** et rester informés des dernières tendances
- Détecter les **mentions de leurs produits** ou services
- Analyser le **sentiment public** sur des sujets spécifiques
- Identifier des **opportunités de marché** émergentes

Cependant, la **surcharge informationnelle** rend cette surveillance manuelle impossible. Il est nécessaire de disposer d'un **système automatisé et intelligent** capable de filtrer, classer et notifier les informations pertinentes en temps réel.

## 1.2 Problématique

Les solutions existantes présentent plusieurs limitations :

| Solution | Avantages | Inconvénients |
|----------|-----------|---------------|
| **Reddit natif** | Gratuit, officiel | Pas de filtres avancés, notifications limitées |
| **IFTTT/Zapier** | Facile à configurer | Limité en fonctionnalités, coûteux |
| **Scripts personnalisés** | Personnalisable | Difficiles à maintenir, non scalables, pas d'UI |

**La problématique centrale** est donc : 

> *Comment concevoir une plateforme moderne, scalable et sécurisée permettant de surveiller Reddit en temps réel avec un filtrage intelligent et des notifications instantanées ?*

## 1.3 Objectifs du Projet

**PipelineGuard Enterprise** vise à développer une solution complète répondant aux objectifs suivants :

1. **Surveillance temps réel** : Intégration avec l'API Reddit (PRAW)
2. **Filtrage intelligent** : Classification automatique par niveau (top/moyen/bas selon score)
3. **Notifications instantanées** : Système WebSocket temps réel
4. **Interface moderne** : Application web responsive avec Angular
5. **Authentification sécurisée** : Gestion utilisateurs avec JWT
6. **Analytics avancés** : Dashboard de statistiques
7. **Architecture scalable** : Microservices containerisés avec Docker

## 1.4 Méthodologie

Le projet a été développé en suivant une **approche agile** :

1. ✅ Analyse des besoins fonctionnels et non-fonctionnels
2. ✅ Conception de l'architecture microservices
3. ✅ Développement itératif backend (FastAPI) et frontend (Angular)
4. ✅ Tests fonctionnels et end-to-end (Playwright)
5. ✅ Déploiement avec Docker Compose

## 1.5 Structure du Rapport

- **Chapitre 2** : Étude du projet (analyse existant, faisabilité, choix techniques)
- **Chapitre 3** : Spécification des besoins (fonctionnels et non-fonctionnels)
- **Chapitre 4** : Conception (architecture, modèle de données, diagrammes)
- **Chapitre 5** : Réalisation (implémentation, tests, déploiement)
- **Chapitre 6** : Conclusion et perspectives
