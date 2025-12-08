# ✅ Liste des Subreddits VALIDES pour Tests

## ❌ ERREUR COMMUNE

**Facebook, Instagram, Twitter ne sont PAS des subreddits!**

Ce sont des réseaux sociaux. Reddit a ses propres communautés appelées "subreddits".

---

## ✅ Subreddits Valides pour Tests

### 🔥 Très Actifs (Recommandés)

| Subreddit | Description | Posts/jour |
|-----------|-------------|------------|
| `python` | Langage Python | ~500 |
| `programming` | Programmation générale | ~300 |
| `javascript` | JavaScript | ~200 |
| `webdev` | Développement web | ~150 |
| `learnprogramming` | Apprentissage | ~400 |

### 💻 Technologies Populaires

| Subreddit | Description |
|-----------|-------------|
| `angular` | Framework Angular |
| `react` | Framework React |
| `vuejs` | Framework Vue.js |
| `nodejs` | Node.js |
| `typescript` | TypeScript |
| `golang` | Go language |
| `rust` | Rust language |
| `cpp` | C++ |
| `java` | Java |
| `csharp` | C# |

### 🚀 Frameworks & Tools

| Subreddit | Description |
|-----------|-------------|
| `fastapi` | FastAPI framework |
| `django` | Django framework |
| `flask` | Flask framework |
| `docker` | Docker |
| `kubernetes` | Kubernetes |
| `devops` | DevOps |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |

### 🎨 Design & Frontend

| Subreddit | Description |
|-----------|-------------|
| `web_design` | Design web |
| `css` | CSS |
| `frontend` | Frontend dev |
| `tailwindcss` | Tailwind CSS |

### 🎮 Autres Populaires

| Subreddit | Description | Type |
|-----------|-------------|------|
| `gaming` | Jeux vidéo | 🎮 |
| `technology` | Technologie | 💻 |
| `science` | Science | 🔬 |
| `news` | Actualités | 📰 |
| `worldnews` | Actualités mondiales | 🌍 |
| `funny` | Humour | 😄 |
| `pics` | Photos | 📷 |
| `videos` | Vidéos | 🎥 |

---

## 🧪 Tests Recommandés

### Test 1: Subreddit Très Actif
```
Subreddit: python
Niveau: top
Résultat attendu: Beaucoup de posts avec scores élevés
```

### Test 2: Subreddit Modéré
```
Subreddit: fastapi
Niveau: moyen
Résultat attendu: Posts avec scores moyens
```

### Test 3: Subreddit Spécialisé
```
Subreddit: angular
Niveau: bas
Résultat attendu: Posts récents, tous niveaux
```

---

## ❌ Erreurs à Éviter

### Ne PAS utiliser:
- ❌ `facebook` → Ce n'est pas un subreddit
- ❌ `instagram` → Ce n'est pas un subreddit
- ❌ `twitter` → Ce n'est pas un subreddit
- ❌ `google` → Ce n'est pas un subreddit
- ❌ `amazon` → Ce n'est pas un subreddit
- ❌ `netflix` → Ce n'est pas un subreddit

### Ces noms donneront:
```
Erreur 404: Le subreddit 'facebook' n'existe pas ou est privé
```

---

## 🔍 Comment Vérifier si un Subreddit Existe?

### Méthode 1: Via Reddit
1. Aller sur https://reddit.com
2. Chercher r/[nom]
3. Si ça existe, vous verrez la page

### Méthode 2: Format URL
```
https://reddit.com/r/python       ✅ Existe
https://reddit.com/r/facebook     ❌ N'existe pas
```

---

## 📊 Niveaux de Score

L'application filtre par score de post:

| Niveau | Score | Description |
|--------|-------|-------------|
| **top** | ≥ 1000 | Posts très populaires |
| **moyen** | 100-999 | Posts populaires |
| **bas** | < 100 | Tous les posts |

---

## 🎯 Exemples Pratiques

### Exemple 1: Développeur Python
```
1. Rechercher: python
2. Niveau: top
3. Résultat: Posts populaires sur Python
```

### Exemple 2: Apprenant Web
```
1. Rechercher: webdev
2. Niveau: moyen
3. Résultat: Tutoriels et discussions web
```

### Exemple 3: News Tech
```
1. Rechercher: technology
2. Niveau: top
3. Résultat: Actualités tech populaires
```

---

## ⚠️ Notes Importantes

### Subreddits Privés
Certains subreddits sont privés ou nécessitent une invitation.
L'application retournera: `404 - Le subreddit n'existe pas ou est privé`

### Subreddits NSFW
L'API Reddit peut bloquer l'accès aux subreddits NSFW selon la configuration.

### Rate Limiting
Reddit limite le nombre de requêtes:
- Ne pas faire plus de 60 requêtes/minute
- Attendre entre les recherches

---

## 🚀 Commandes de Test

### Backend - Test Manuel
```bash
# Tester avec subreddit valide
curl -X GET "http://localhost:8000/search?q=python" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Tester avec subreddit invalide
curl -X GET "http://localhost:8000/search?q=facebook" \
  -H "Authorization: Bearer YOUR_TOKEN"
# Résultat attendu: 404
```

### Frontend - Tests UI
1. Aller sur `/subscribe`
2. Essayer "python" → ✅ Doit marcher
3. Essayer "facebook" → ❌ Erreur 404 (normal)

---

## 📝 Checklist de Test

- [ ] Tester avec "python" (doit marcher)
- [ ] Tester avec "angular" (doit marcher)
- [ ] Tester avec "fastapi" (doit marcher)
- [ ] Tester avec "facebook" (doit échouer proprement)
- [ ] Vérifier les 3 niveaux (top, moyen, bas)
- [ ] S'abonner à 2-3 subreddits
- [ ] Vérifier /my_posts

---

## 💡 Astuce

**Pour découvrir de nouveaux subreddits:**
1. Aller sur https://reddit.com
2. Explorer les catégories
3. Chercher r/[votre_intérêt]
4. Copier le nom (sans r/)
5. L'utiliser dans l'application

---

## ✅ Résumé

**À UTILISER:**
- ✅ python, angular, programming, webdev, javascript, react, etc.
- ✅ Tous les vrais subreddits Reddit

**À NE PAS UTILISER:**
- ❌ facebook, instagram, twitter, google
- ❌ Noms de réseaux sociaux ou entreprises

**L'application fonctionne parfaitement avec de vrais subreddits!** 🎉
