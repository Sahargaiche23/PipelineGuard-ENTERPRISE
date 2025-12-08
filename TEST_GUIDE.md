# 🧪 Guide de Test - PipelineGuard Enterprise

## ✅ Corrections Appliquées

### 1. **Erreur 500 sur /search**
- ✅ Meilleure gestion des erreurs
- ✅ Validation du subreddit
- ✅ Vérification authentification Reddit
- ✅ Messages d'erreur détaillés

### 2. **Erreur 422 sur /subscribe**
- ✅ Validation des niveaux ("top", "moyen", "bas")
- ✅ Message d'erreur explicite si niveau invalide
- ✅ Frontend déjà configuré avec les bonnes valeurs

### 3. **Navbar sur toutes les pages**
- ✅ Profile
- ✅ My Posts
- ✅ Analytics
- ✅ Feed

---

## 🧪 Tests à Effectuer

### Test 1: Recherche Reddit

#### ✅ Test avec subreddit valide
```
Endpoint: GET /search?q=python
Résultat attendu: 200 OK avec liste de posts
```

**Dans le frontend:**
1. Aller sur `/subscribe`
2. Rechercher "python"
3. ✅ Doit afficher les posts

#### ❌ Test avec subreddit invalide
```
Endpoint: GET /search?q=qsdjfhqskldfh
Résultat attendu: 404 avec message "Le subreddit n'existe pas"
```

#### ❌ Test avec champ vide
```
Endpoint: GET /search?q=
Résultat attendu: 400 avec message "Le nom du subreddit est requis"
```

---

### Test 2: Abonnement

#### ✅ Test avec niveau valide
```
Endpoint: POST /subscribe
Body: topic=python, level=top
Résultat attendu: 200 OK avec message de succès
```

**Dans le frontend:**
1. Aller sur `/subscribe`
2. Saisir "python"
3. **Sélectionner "Top" dans la liste déroulante** (ne pas taper à la main)
4. Cliquer "S'abonner"
5. ✅ Message: "Abonnement enregistré et notification créée"

#### ❌ Test avec niveau invalide (si saisi manuellement)
```
Endpoint: POST /subscribe
Body: topic=facebook, level=haut
Résultat attendu: 422 avec message "Niveau invalide"
```

**Niveaux valides uniquement:**
- `bas`
- `moyen`
- `top`

---

### Test 3: Mes Posts

#### ✅ Test liste vide
```
Endpoint: GET /my_posts
Résultat attendu: 200 OK avec []
```

**Normal si aucun abonnement ou aucun post dans les subreddits abonnés**

#### ✅ Test avec abonnement
1. S'abonner à "python" niveau "top"
2. GET /my_posts
3. ✅ Doit afficher les posts de r/python

---

### Test 4: Navigation

#### Test Navbar
1. Se connecter
2. Aller sur `/profile` → ✅ Navbar visible
3. Aller sur `/my-posts` → ✅ Navbar visible
4. Aller sur `/analytics` → ✅ Navbar visible
5. Aller sur `/feed` → ✅ Navbar visible
6. Aller sur `/subscribe` → ✅ Navbar visible
7. Aller sur `/notifications` → ✅ Navbar visible

#### Test Liens Navbar
1. Cliquer "Fil d'actualité" → `/feed`
2. Cliquer "Mes Posts" → `/my-posts`
3. Cliquer "Analytics" → `/analytics`
4. Cliquer "Abonnements" → `/subscribe`
5. Cliquer "Notifications" → `/notifications`
6. Menu utilisateur → "Mon Profil" → `/profile`

---

## 🐛 Erreurs Connues Résolues

### ❌ "Erreur lors de la recherche Reddit"
**Cause:** 
- Username avec espace dans config.py
- Subreddit inexistant
- Credentials Reddit invalides

**Solution:**
- ✅ Espace supprimé dans username
- ✅ Validation du subreddit ajoutée
- ✅ Vérification authentification Reddit
- ✅ Messages d'erreur détaillés

### ❌ Validation Error sur /subscribe
**Cause:**
- Niveau "haut" saisi manuellement au lieu de sélectionner

**Solution:**
- ✅ Validation backend ajoutée
- ✅ Message d'erreur explicite
- ✅ Frontend utilise déjà les bonnes valeurs dans le select

### ❌ Navbar manquante
**Cause:**
- `<app-navbar>` non ajouté sur nouvelles pages

**Solution:**
- ✅ Ajouté sur profile, my-posts, analytics, feed

---

## 📝 Checklist Complète

### Backend
- [x] config.py: username sans espace
- [x] main.py: Validation /search améliorée
- [x] main.py: Validation /subscribe avec niveaux
- [x] main.py: Meilleure gestion erreurs
- [x] requirements.txt: Toutes les dépendances
- [x] init_db.py: Script d'initialisation

### Frontend
- [x] Navbar sur profile
- [x] Navbar sur my-posts
- [x] Navbar sur analytics
- [x] Navbar sur feed
- [x] Navbar sur subscribe (déjà présente)
- [x] Navbar sur notifications (déjà présente)
- [x] Subscribe: Niveaux corrects dans select

### Documentation
- [x] QUICK_START.md
- [x] START_APP.sh
- [x] CORRECTIONS_APPLIQUEES.md
- [x] TEST_GUIDE.md (ce fichier)
- [x] RUN_APPLICATION.md
- [x] FEATURES_ADDED.md

---

## 🚀 Commandes de Test

### Tester Backend Manuellement

```bash
# Démarrer le backend
cd backend
uvicorn main:app --reload

# Dans un autre terminal, tester les endpoints
# Test search valide
curl -X GET "http://localhost:8000/search?q=python" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test search invalide
curl -X GET "http://localhost:8000/search?q=qsdfqsdf" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test subscribe valide
curl -X POST "http://localhost:8000/subscribe?topic=python&level=top" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test subscribe invalide
curl -X POST "http://localhost:8000/subscribe?topic=python&level=haut" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Obtenir un Token

```bash
# Register
curl -X POST "http://localhost:8000/register?username=test&password=test123"

# Login
curl -X POST "http://localhost:8000/login?username=test&password=test123"
# Copier le access_token de la réponse
```

---

## 💡 Conseils de Test

### Subreddits Recommandés pour les Tests

**Subreddits populaires (toujours actifs):**
- `python` - Posts Python
- `angular` - Posts Angular
- `fastapi` - Posts FastAPI
- `programming` - Posts programmation générale
- `webdev` - Posts développement web

**Subreddits inexistants (pour tester les erreurs):**
- `qsdfqsdfqsdf`
- `zzzzzzzzzzzz`
- `testinvalidsubreddit`

### Niveaux à Tester

- **bas** - Posts avec score < 100
- **moyen** - Posts avec 100 ≤ score < 1000
- **top** - Posts avec score ≥ 1000

---

## 🎯 Résultat Attendu Final

Après tous les tests:

1. ✅ Recherche Reddit fonctionne avec subreddits valides
2. ✅ Erreur 404 sur subreddits invalides (message clair)
3. ✅ Abonnement fonctionne avec niveaux valides
4. ✅ Erreur 422 sur niveaux invalides (message clair)
5. ✅ Navbar visible sur toutes les pages
6. ✅ Navigation fluide entre toutes les pages
7. ✅ Pas d'erreurs 500 non gérées

**Application 100% fonctionnelle! 🎉**

---

## 🆘 Dépannage

### Si /search retourne toujours 500
1. Vérifier les logs du terminal backend
2. Vérifier que les credentials Reddit sont valides
3. Tester l'authentification: `reddit.user.me()`
4. Essayer avec un subreddit très connu: "python"

### Si /subscribe retourne 422
1. Vérifier que le niveau est "bas", "moyen" ou "top"
2. Ne PAS taper manuellement, utiliser le select
3. Vérifier les logs backend pour voir la valeur reçue

### Si la navbar ne s'affiche pas
1. Vérifier que le composant navbar est déclaré dans app.module.ts
2. Recompiler Angular: `ng serve`
3. Vider le cache du navigateur (Ctrl+Shift+R)

---

## ✅ Tests Réussis

Une fois tous les tests passés, l'application est prête!

**Prochain test recommandé:**
1. Créer un compte
2. Configurer le profil avec avatar
3. S'abonner à 2-3 subreddits
4. Créer quelques posts avec images
5. Interagir (likes, commentaires)
6. Consulter les analytics

**Bonne utilisation! 🚀**
