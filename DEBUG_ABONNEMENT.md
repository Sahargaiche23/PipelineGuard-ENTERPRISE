# 🐛 Debug: Abonnement ne se crée pas

## Problèmes Identifiés

1. ❌ Message "Vous devez vous connecter avant de vous abonner"
2. ❌ Abonnements ne se créent pas
3. ❌ Notifications ne s'affichent pas
4. ❌ Analytics affichent 0 partout

## Diagnostic

### Étape 1: Vérifier si vous êtes vraiment connecté

**Ouvrir la Console du Navigateur (F12):**

```javascript
// Dans l'onglet Console, taper:
localStorage.getItem('access_token')
```

**Résultats possibles:**

✅ **Si retourne un token (long string):**
```
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYW1hcnNhaGFyIi..."
```
→ Vous êtes connecté, le problème est ailleurs

❌ **Si retourne `null`:**
```
null
```
→ Vous n'êtes PAS connecté, il faut se reconnecter

---

### Étape 2: Se Reconnecter Proprement

**Solution Complète:**

1. **Déconnexion:**
```javascript
// Dans Console (F12)
localStorage.clear()
```

2. **Fermer tous les onglets** de l'application

3. **Redémarrer le Frontend:**
```bash
cd front/projet
# Ctrl+C pour arrêter
ng serve
```

4. **Rouvrir:** http://localhost:4200

5. **Se Connecter:**
   - Username: votre_username
   - Password: votre_password

6. **Vérifier le token:**
```javascript
// Console (F12)
localStorage.getItem('access_token')
// Devrait afficher un long string
```

---

### Étape 3: Tester l'Abonnement

**Après reconnexion:**

1. Aller sur `/subscribe`
2. Subreddit: `python`
3. Niveau: `top`
4. Cliquer "S'abonner"

**Résultat Attendu:**
✅ Message: "Abonnement enregistré et notification créée"

**Si toujours erreur:**
Ouvrir Console (F12) et regarder les erreurs

---

## Solutions par Scénario

### Scénario A: Token = null (Pas connecté)

**Solution:**
```bash
1. Se déconnecter
2. Vider le cache: localStorage.clear()
3. Se reconnecter
```

### Scénario B: Token existe mais erreur 401

**Cause:** Token expiré ou invalide

**Solution:**
```bash
1. Déconnexion
2. Reconnexion
```

### Scénario C: Token existe, pas d'erreur, mais rien ne se passe

**Cause:** Backend pas démarré ou problème CORS

**Solution:**
```bash
# Vérifier que le backend tourne
curl http://localhost:8000/docs
# Devrait retourner du HTML

# Si erreur, redémarrer backend:
cd backend
uvicorn main:app --reload
```

---

## Vérification Backend

### Test 1: Backend actif
```bash
curl http://localhost:8000/docs
```
✅ Devrait afficher la doc Swagger

### Test 2: Abonnement manuel
```bash
# D'abord login pour obtenir le token
TOKEN=$(curl -X POST "http://localhost:8000/login?username=samarsahar&password=VOTRE_PASSWORD" | jq -r '.access_token')

# Puis tester subscribe
curl -X POST "http://localhost:8000/subscribe?topic=python&level=top" \
  -H "Authorization: Bearer $TOKEN"
```

✅ Devrait retourner: `{"message":"Abonnement enregistré..."}`

---

## Fix Frontend si Token n'est pas sauvegardé

**Si le login ne sauvegarde pas le token:**

### Vérifier login.component.ts

Le code doit être:
```typescript
this.authService.login(this.username, this.password).subscribe({
  next: (response: any) => {
    console.log('Token reçu:', response.access_token); // AJOUTER CE LOG
    this.authService.setToken(response.access_token);
    
    // VÉRIFIER IMMÉDIATEMENT
    console.log('Token sauvegardé:', localStorage.getItem('access_token')); 
    
    this.router.navigate(['/notifications']);
  }
});
```

**Tester:**
1. Se connecter
2. Regarder Console (F12)
3. Devrait voir les 2 logs avec le même token

---

## Fix WebSocket (Notifications)

**Si les notifications ne s'affichent pas:**

### Problème: WebSocket ne se connecte pas

**Dans Console (F12), chercher:**
```
WebSocket connection to 'ws://localhost:8000/ws/...' failed
```

**Solution:**
1. Backend doit tourner
2. Token doit être valide

**Test WebSocket:**
```javascript
// Console (F12)
const token = localStorage.getItem('access_token');
const ws = new WebSocket(`ws://localhost:8000/ws/${token}`);
ws.onopen = () => console.log('✅ WebSocket connecté!');
ws.onerror = (e) => console.error('❌ WebSocket erreur:', e);
```

---

## Checklist Complète

### Avant de tester:
- [ ] Backend tourne (port 8000)
- [ ] Frontend tourne (port 4200)
- [ ] Zookeeper et Kafka2 démarrés

### Pour se connecter:
- [ ] localStorage.clear() fait
- [ ] Se déconnecter si déjà connecté
- [ ] Fermer tous les onglets
- [ ] Rouvrir navigateur
- [ ] Se connecter
- [ ] Vérifier token dans Console: `localStorage.getItem('access_token')`

### Pour s'abonner:
- [ ] Token existe dans localStorage
- [ ] Aller sur /subscribe
- [ ] Entrer un subreddit VALIDE (ex: python, angular)
- [ ] Choisir niveau (top, moyen, bas)
- [ ] Cliquer S'abonner
- [ ] Vérifier message de succès

### Pour voir les notifications:
- [ ] Backend tourne
- [ ] Token valide
- [ ] WebSocket connecté (voir Console)
- [ ] Badge navbar affiche le nombre

---

## Commandes de Redémarrage Complet

```bash
# Terminal 1: Backend
cd backend
pkill -f uvicorn
python3 fix_existing_users.py  # Pour analytics
uvicorn main:app --reload

# Terminal 2: Frontend
cd front/projet
pkill -f "ng serve"
ng serve

# Terminal 3: Docker
docker restart zookeeper kafka2
```

**Attendre 30 secondes que tout démarre**

---

## Tests de Validation

### Test 1: Connexion
```
1. http://localhost:4200/login
2. Se connecter
3. Console (F12): localStorage.getItem('access_token')
4. ✅ Doit afficher un token
```

### Test 2: Subscribe
```
1. http://localhost:4200/subscribe
2. Subreddit: python
3. Niveau: top
4. S'abonner
5. ✅ Message: "Abonnement enregistré"
```

### Test 3: Analytics
```
1. http://localhost:4200/analytics
2. ✅ Total abonnements: 1 (ou plus)
3. ✅ Répartition: Top = 1
```

### Test 4: Notifications
```
1. Badge navbar
2. ✅ Affiche un nombre > 0
3. Cliquer dessus
4. ✅ Liste des notifications
```

---

## Si Rien ne Fonctionne

### Reset Complet

```bash
# 1. Arrêter tout
pkill -f uvicorn
pkill -f "ng serve"
docker stop zookeeper kafka2

# 2. Nettoyer
cd backend
rm -f pipelineguard.db
python3 init_db.py

# 3. Redémarrer
docker start zookeeper kafka2
sleep 5
uvicorn main:app --reload &

cd ../front/projet
ng serve &

# 4. Browser
# - Fermer tous les onglets
# - localStorage.clear()
# - Rouvrir http://localhost:4200
# - Créer NOUVEAU compte
# - Tester abonnement
```

---

## Logs à Vérifier

### Backend (Terminal)
```
✅ "Uvicorn running on http://0.0.0.0:8000"
✅ "Application startup complete"
```

### Frontend (Terminal)
```
✅ "✔ Compiled successfully"
✅ "Angular Live Development Server is listening"
```

### Browser Console (F12)
```
✅ Pas d'erreur 401
✅ Pas d'erreur CORS
✅ Pas d'erreur WebSocket (sauf si pas abonné)
```

---

## ✅ Solution Rapide

**Pour 90% des cas:**

```bash
# 1. Dans Console Browser (F12)
localStorage.clear()

# 2. Fermer navigateur complètement

# 3. Rouvrir http://localhost:4200

# 4. Se reconnecter

# 5. Tester abonnement
```

**Ça devrait marcher! 🎉**
