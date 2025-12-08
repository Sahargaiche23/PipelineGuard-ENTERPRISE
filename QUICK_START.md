# 🚀 Guide de Démarrage Rapide - PipelineGuard Enterprise

## ⚡ Démarrage en 3 étapes

### 1️⃣ Démarrer les services Docker

```bash
docker start zookeeper
docker start kafka
```

### 2️⃣ Démarrer le Backend

```bash
cd backend

# Installer les dépendances (première fois seulement)
pip install -r requirements.txt

# Initialiser la base de données (première fois seulement)
python init_db.py

# Démarrer le serveur FastAPI
uvicorn main:app --reload
```

**Backend disponible sur:** http://localhost:8000

### 3️⃣ Démarrer le Frontend

**Nouveau terminal:**

```bash
cd front/projet

# Installer les dépendances (première fois seulement)
npm install

# Démarrer Angular
ng serve
```

**Frontend disponible sur:** http://localhost:4200

---

## 🎯 Pages Disponibles

Après connexion, vous pouvez accéder à:

| URL | Description | Navbar |
|-----|-------------|--------|
| `/login` | Connexion | ❌ |
| `/register` | Inscription | ❌ |
| `/feed` | 🌐 Fil d'actualité social | ✅ |
| `/my-posts` | 📝 Créer et gérer vos posts | ✅ |
| `/profile` | 👤 Gérer votre profil | ✅ |
| `/analytics` | 📊 Tableau de bord analytics | ✅ |
| `/subscribe` | 🔔 Abonnements Reddit | ✅ |
| `/notifications` | 📬 Notifications | ✅ |

**✅ Toutes les nouvelles pages ont la navbar!**

---

## 🐛 Résolution des Problèmes

### Erreur 500 sur /search
✅ **Corrigé** - Espace supprimé du username Reddit dans `config.py`

### Navbar manquante
✅ **Corrigé** - `<app-navbar></app-navbar>` ajouté sur toutes les pages:
- profile.component.html
- my-posts.component.html
- analytics.component.html
- feed.component.html

### Posts ne se chargent pas
✅ **Corrigé** - Vérifiez que:
1. La base de données est initialisée: `python init_db.py`
2. Le backend est démarré
3. Vous êtes connecté

---

## 🔧 Commandes Utiles

### Backend
```bash
# Voir les logs du backend
cd backend
uvicorn main:app --reload

# Réinitialiser la base de données
python init_db.py

# Tester un endpoint
curl -X GET http://localhost:8000/posts \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Frontend
```bash
# Recompiler Angular
cd front/projet
ng serve --open

# Nettoyer et réinstaller
rm -rf node_modules package-lock.json
npm install
```

### Docker
```bash
# Vérifier que les conteneurs tournent
docker ps

# Voir les logs
docker logs kafka
docker logs zookeeper

# Redémarrer
docker restart zookeeper kafka
```

---

## 📱 Tester les Fonctionnalités

### 1. Créer un compte
1. Aller sur http://localhost:4200
2. Cliquer sur "S'inscrire"
3. Créer un compte

### 2. Configurer le profil
1. Aller sur `/profile`
2. Cliquer sur "Modifier le profil"
3. **Upload d'avatar** - Choisir une image
4. Remplir email, nom, bio
5. Enregistrer

### 3. Créer un post
1. Aller sur `/my-posts`
2. Cliquer sur "Créer un nouveau post"
3. Ajouter titre et contenu
4. **Upload d'image** - Joindre une image
5. Cliquer sur "Créer"

### 4. Interagir sur le feed
1. Aller sur `/feed`
2. **Liker** un post ❤️
3. **Commenter** - Écrire et envoyer
4. **Partager** - Partager sur votre profil

### 5. Voir les analytics
1. Aller sur `/analytics`
2. Consulter vos statistiques
3. Voir votre niveau d'activité
4. Analyser votre engagement

---

## ✅ Checklist de Vérification

- [ ] Zookeeper démarré (`docker ps`)
- [ ] Kafka démarré (`docker ps`)
- [ ] Base de données initialisée (`python init_db.py`)
- [ ] Backend tourne sur port 8000
- [ ] Frontend tourne sur port 4200
- [ ] Peut se connecter
- [ ] Navbar visible sur toutes les pages
- [ ] Peut créer un post avec image
- [ ] Peut liker/commenter/partager
- [ ] Analytics s'affichent

---

## 🎨 Nouvelles Fonctionnalités

### ✨ Ce qui a été ajouté:

1. **👤 Profil Complet**
   - Upload d'avatar
   - Modification d'informations
   - Suppression de compte

2. **📝 Posts avec Images**
   - Création de posts
   - Upload d'images
   - Modification et suppression

3. **🌐 Interactions Sociales**
   - Likes (toggle)
   - Commentaires avec CRUD
   - Partage de posts

4. **📊 Analytics Dashboard**
   - Vue d'ensemble du compte
   - Statistiques complètes
   - Taux d'engagement
   - Niveaux d'activité

5. **🎯 Navbar sur Toutes les Pages**
   - Navigation cohérente
   - Liens vers toutes les fonctionnalités
   - Menu utilisateur avec avatar

---

## 🆘 Support

En cas de problème:

1. Vérifier les logs du terminal backend
2. Vérifier les logs du navigateur (F12 → Console)
3. S'assurer que tous les services sont démarrés
4. Réinitialiser la base de données si nécessaire

---

## 🎉 C'est Prêt!

Votre plateforme sociale PipelineGuard Enterprise est maintenant complète avec:
- ✅ Navbar sur toutes les pages
- ✅ Upload d'images (avatar + posts)
- ✅ Interactions sociales complètes
- ✅ Analytics avancés
- ✅ Design moderne et responsive

**Bon développement! 🚀**
