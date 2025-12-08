# ❌ Erreur: "Niveau invalide. Doit être: top, moyen, bas"

## Problème

Vous avez reçu une erreur **422 Unprocessable Entity** avec le message:
```
"detail": "Niveau invalide. Doit être: top, moyen, bas"
```

## Cause

Vous avez **tapé manuellement "haut"** au lieu de **sélectionner dans la liste**.

### Valeurs INCORRECTES ❌
- `haut` ❌
- `élevé` ❌
- `high` ❌
- `Top` ❌ (majuscule)
- `TOP` ❌ (tout majuscule)

### Valeurs CORRECTES ✅
- `bas` ✅ (tout en minuscule)
- `moyen` ✅ (tout en minuscule)
- `top` ✅ (tout en minuscule)

---

## Solution

### ✅ UTILISER la Liste Déroulante

**Ne PAS taper manuellement!**

Le formulaire a maintenant 3 options claires:

1. **🔹 Bas** (score < 100)
   - Posts récents, tous niveaux
   - Valeur: `bas`

2. **🔸 Moyen** (score 100-999)
   - Posts avec engagement modéré
   - Valeur: `moyen`

3. **🔥 Top** (score ≥ 1000)
   - Posts très populaires
   - Valeur: `top`

---

## Comment S'abonner Correctement

### Étape 1: Aller sur /subscribe
```
http://localhost:4200/subscribe
```

### Étape 2: Remplir le Formulaire

**Nom du Subreddit:**
```
python
```
(Subreddit valide, sans r/)

**Niveau:**
```
Cliquer sur la liste déroulante
Choisir: 🔥 Top
```
**NE PAS taper "haut" manuellement!**

### Étape 3: S'abonner
```
Cliquer sur le bouton "S'abonner"
```

### Résultat Attendu
```
✅ "Abonnement enregistré et notification créée"
```

---

## Exemples Corrects

### Exemple 1: Python - Top
```
Subreddit: python
Niveau: 🔥 Top (depuis la liste)
Résultat: ✅ Abonnement créé
```

### Exemple 2: Angular - Moyen
```
Subreddit: angular
Niveau: 🔸 Moyen (depuis la liste)
Résultat: ✅ Abonnement créé
```

### Exemple 3: Programming - Bas
```
Subreddit: programming
Niveau: 🔹 Bas (depuis la liste)
Résultat: ✅ Abonnement créé
```

---

## Exemples INCORRECTS

### ❌ Exemple 1: Taper "haut"
```
Subreddit: tiktok
Niveau: haut (tapé manuellement)
Résultat: ❌ Erreur 422 "Niveau invalide"
```

### ❌ Exemple 2: Majuscule
```
Subreddit: python
Niveau: Top (avec majuscule)
Résultat: ❌ Erreur 422 "Niveau invalide"
```

### ❌ Exemple 3: Anglais
```
Subreddit: python
Niveau: high
Résultat: ❌ Erreur 422 "Niveau invalide"
```

---

## Validation Backend

Le backend valide strictement les niveaux:

```python
valid_levels = ["top", "moyen", "bas"]
if level not in valid_levels:
    raise HTTPException(
        status_code=422, 
        detail=f"Niveau invalide. Doit être: {', '.join(valid_levels)}"
    )
```

**Règles:**
- ✅ Tout en minuscule
- ✅ Exactement: "top", "moyen" ou "bas"
- ❌ Pas de majuscules
- ❌ Pas d'autres mots
- ❌ Pas de traductions

---

## Signification des Niveaux

### 🔹 Bas (score < 100)
**Quand l'utiliser:**
- Vous voulez TOUS les posts
- Posts récents même peu populaires
- Découvrir du contenu nouveau

**Exemple:**
```
r/python niveau "bas" → Tous les posts, même avec 5 upvotes
```

### 🔸 Moyen (score 100-999)
**Quand l'utiliser:**
- Contenu moyennement populaire
- Équilibre entre qualité et quantité
- Posts avec un engagement correct

**Exemple:**
```
r/angular niveau "moyen" → Posts avec 100-999 upvotes
```

### 🔥 Top (score ≥ 1000)
**Quand l'utiliser:**
- Seulement le meilleur contenu
- Posts très populaires
- Annonces importantes

**Exemple:**
```
r/programming niveau "top" → Posts avec 1000+ upvotes
```

---

## Correction Appliquée

### Interface Améliorée

Le formulaire affiche maintenant:

```html
Niveau (sélectionner uniquement)
[Liste déroulante]
  🔹 Bas (score < 100)
  🔸 Moyen (score 100-999)
  🔥 Top (score ≥ 1000)

⚠️ Ne pas taper "haut"! Utilisez la liste déroulante
```

**Avantages:**
- ✅ Impossible de se tromper
- ✅ Indication visuelle claire
- ✅ Explication des scores
- ✅ Message d'avertissement

---

## Test de Validation

### Test Correct ✅
```bash
1. Aller sur /subscribe
2. Subreddit: python
3. Cliquer liste déroulante "Niveau"
4. Choisir: 🔥 Top
5. Cliquer "S'abonner"
6. ✅ Message: "Abonnement enregistré"
```

### Test Incorrect ❌
```bash
1. Aller sur /subscribe
2. Subreddit: tiktok
3. Taper manuellement dans Niveau: "haut"
4. Cliquer "S'abonner"
5. ❌ Erreur 422: "Niveau invalide"
```

**Note:** Avec la correction, il est maintenant impossible de taper manuellement dans le champ Niveau.

---

## API Backend - Référence

### Endpoint: POST /subscribe

**Paramètres:**
- `topic` (string): Nom du subreddit (ex: "python")
- `level` (string): **DOIT ÊTRE** "bas", "moyen" ou "top"

**Exemple cURL correct:**
```bash
curl -X POST "http://localhost:8000/subscribe?topic=python&level=top" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Réponse Succès (200):**
```json
{
  "message": "Abonnement enregistré et notification créée"
}
```

**Réponse Erreur (422):**
```json
{
  "detail": "Niveau invalide. Doit être: top, moyen, bas"
}
```

---

## Subreddits Valides

**Rappel:** Utilisez des subreddits **réels** de Reddit:

✅ **Valides:**
- python
- angular
- programming
- webdev
- javascript
- react
- fastapi
- django

❌ **Invalides:**
- tiktok (pas un subreddit, c'est un réseau social)
- facebook (pas un subreddit)
- instagram (pas un subreddit)

---

## Résumé

### ✅ À FAIRE
1. Utiliser la liste déroulante
2. Choisir: Bas, Moyen ou Top
3. Ne rien taper manuellement
4. Utiliser des subreddits valides

### ❌ À NE PAS FAIRE
1. Taper "haut" manuellement
2. Utiliser des majuscules
3. Traduire en anglais (high, low)
4. Inventer des niveaux

---

## ✅ Problème Résolu!

Avec la correction appliquée:
- Interface plus claire
- Impossible de se tromper
- Messages explicites
- Validation visuelle

**Plus d'erreur 422 possible sur les niveaux! 🎉**
