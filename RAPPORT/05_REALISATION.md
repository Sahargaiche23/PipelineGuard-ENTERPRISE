# 5. Réalisation

## 5.1 Environnement de Développement

### 5.1.1 Outils et Logiciels

| Catégorie | Outil | Version | Utilisation |
|-----------|-------|---------|-------------|
| **IDE** | VS Code | 1.85+ | Développement backend/frontend |
| **Python** | Python | 3.11.5 | Runtime backend |
| **Node.js** | Node.js | 18.17 LTS | Build frontend |
| **Database** | PostgreSQL | 15 | Production |
| **Database** | SQLite | 3.x | Développement |
| **Container** | Docker | 24.0.6 | Containerisation |
| **Container** | Docker Compose | 2.21.0 | Orchestration |
| **Git** | Git | 2.42 | Versioning |
| **API Testing** | Postman | 10.18 | Test endpoints |
| **Browser** | Chrome | 118+ | Tests frontend |

### 5.1.2 Extensions VS Code Utilisées

- **Python** : Linting, debugging
- **Angular Language Service** : Autocomplétion TypeScript
- **Docker** : Gestion conteneurs
- **GitLens** : Historique Git enrichi
- **REST Client** : Test API directement dans VSCode

### 5.1.3 Structure du Projet

```
PipelineGuard-ENTERPRISE/
├── backend/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── auth.py              # Routes authentification
│   ├── posts.py             # Routes gestion posts
│   ├── analytics.py         # Routes analytics
│   ├── models.py            # Modèles SQLAlchemy
│   ├── database.py          # Configuration DB
│   ├── config.py            # Configuration Reddit
│   ├── websocket_manager.py # Gestionnaire WebSocket
│   ├── requirements.txt     # Dépendances Python
│   └── test.db              # SQLite développement
│
├── front/
│   └── projet/
│       ├── src/
│       │   └── app/
│       │       ├── components/  # Composants Angular
│       │       ├── services/    # Services
│       │       └── guards/      # Guards routing
│       ├── package.json
│       └── angular.json
│
├── docker-compose.yml       # Orchestration services
├── Dockerfile.backend
├── Dockerfile.frontend
├── nginx.conf
├── consumer.py              # Kafka consumer
├── producer.py              # Kafka producer
└── README.md
```

## 5.2 Implémentation Backend

### 5.2.1 Configuration FastAPI

**main.py** - Configuration de base :
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PipelineGuard Enterprise API",
    version="1.0.0",
    description="API de surveillance Reddit"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(analytics_router)
```

### 5.2.2 Authentification JWT

**auth.py** - Génération et validation tokens :
```python
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "supersecret"  # En prod : variable d'environnement
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    return user
```

**Points clés** :
- ✅ Bcrypt pour hachage passwords (12 rounds)
- ✅ JWT avec expiration automatique
- ✅ Dependency injection pour get_current_user()

### 5.2.3 Intégration Reddit API (PRAW)

**main.py** - Recherche et abonnement :
```python
import praw
from config import REDDIT_CONFIG

@app.get("/search")
async def search_posts(q: str, current_user: User = Depends(get_current_user)):
    reddit = praw.Reddit(
        client_id=REDDIT_CONFIG['client_id'],
        client_secret=REDDIT_CONFIG['client_secret'],
        username=REDDIT_CONFIG['username'],
        password=REDDIT_CONFIG['password'],
        user_agent=REDDIT_CONFIG['user_agent']
    )
    
    # Vérifier existence subreddit
    subreddit = reddit.subreddit(q)
    _ = subreddit.id  # Lève exception si inexistant
    
    results = []
    for post in subreddit.hot(limit=20):
        level = "top" if post.score >= 1000 else "moyen" if post.score >= 100 else "bas"
        results.append({
            "id": post.id,
            "title": post.title,
            "level": level,
            "url": post.url,
            "author": str(post.author),
            "created_utc": float(post.created_utc)
        })
    return results
```

**Gestion des erreurs** :
- ✅ Subreddit inexistant → 404
- ✅ Subreddit privé → 404
- ✅ Erreur authentification Reddit → 500

### 5.2.4 WebSocket Temps Réel

**main.py** - Endpoint WebSocket :
```python
from fastapi import WebSocket
import asyncio
import json

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await websocket.accept()
    
    # Validation JWT
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    
    # Enregistrement connexion
    await manager.connect(username, websocket)
    
    # Envoi notifications existantes
    notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
    for notif in notifications:
        await websocket.send_text(json.dumps({
            "id": notif.id,
            "title": "Notification Reddit",
            "content": notif.content,
            "created_at": str(notif.created_at)
        }))
    
    # Boucle de polling
    while True:
        await asyncio.sleep(5)
        new_notifications = db.query(Notification).filter(...).all()
        for notif in new_notifications:
            await websocket.send_text(json.dumps(notif_dict))
```

**Stratégie** : Polling toutes les 5 secondes pour détecter nouvelles notifications.

### 5.2.5 Analytics

**analytics.py** - Statistiques d'abonnements :
```python
from sqlalchemy import func

@router.get("/analytics/subscriptions")
async def get_subscriptions_analytics(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    
    # Total
    total = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).count()
    
    # Par niveau
    by_level = db.query(
        Subscription.level,
        func.count(Subscription.id).label('count')
    ).filter(
        Subscription.user_id == current_user.id
    ).group_by(Subscription.level).all()
    
    return {
        "total": total,
        "by_level": {
            "top": level_data.get("top", 0),
            "moyen": level_data.get("moyen", 0),
            "bas": level_data.get("bas", 0)
        }
    }
```

**Requêtes optimisées** : Utilisation de GROUP BY pour aggrégations.

## 5.3 Implémentation Frontend

### 5.3.1 AuthService

**auth.service.ts** - Gestion authentification :
```typescript
@Injectable({ providedIn: 'root' })
export class AuthService {
  private tokenKey = 'access_token';

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>('/login', { username, password })
      .pipe(
        tap(response => {
          localStorage.setItem(this.tokenKey, response.access_token);
        })
      );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    return localStorage.getItem(this.tokenKey) !== null;
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }
}
```

### 5.3.2 HTTP Interceptor JWT

**Ajout automatique du token** :
```typescript
@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();
    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }
    return next.handle(request);
  }
}
```

### 5.3.3 WebSocket Service

**websocket.service.ts** :
```typescript
@Injectable({ providedIn: 'root' })
export class WebSocketService {
  private socket: WebSocket | null = null;
  public notifications$ = new Subject<Notification>();

  connect(token: string): void {
    this.socket = new WebSocket(`ws://localhost:8000/ws/${token}`);
    
    this.socket.onmessage = (event) => {
      const notification = JSON.parse(event.data);
      this.notifications$.next(notification);
    };
    
    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close();
    }
  }
}
```

### 5.3.4 Composant Subscribe

**subscribe.component.ts** - Recherche et abonnement :
```typescript
export class SubscribeComponent implements OnInit {
  searchTerm: string = '';
  posts: any[] = [];
  selectedLevel: string = 'top';

  search(): void {
    this.httpService.get(`/search?q=${this.searchTerm}`)
      .subscribe({
        next: (data) => {
          this.posts = data;
        },
        error: (err) => {
          alert(err.error.detail);
        }
      });
  }

  subscribe(): void {
    this.httpService.post('/subscribe', {
      topic: this.searchTerm,
      level: this.selectedLevel
    }).subscribe({
      next: () => {
        alert('Abonnement créé avec succès !');
      }
    });
  }
}
```

## 5.4 Tests

### 5.4.1 Tests End-to-End (Playwright)

**Structure** :
```
front/projet/e2e/
├── login.spec.ts
├── register.spec.ts
└── subscribe.spec.ts
```

**Exemple - login.spec.ts** :
```typescript
import { test, expect } from '@playwright/test';

test('should login successfully', async ({ page }) => {
  await page.goto('http://localhost:4200');
  
  await page.fill('input[name="username"]', 'testuser');
  await page.fill('input[name="password"]', 'testpass');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('http://localhost:4200/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

**Commandes Playwright** :

#### Installation
```bash
# Installer Playwright
npm install -D @playwright/test

# Installer les navigateurs
npx playwright install

# Installer navigateurs avec dépendances système
npx playwright install --with-deps
```

#### Exécution des Tests
```bash
# Exécuter tous les tests (headless)
npx playwright test

# Exécuter avec interface graphique
npx playwright test --ui

# Exécuter en mode headed (navigateur visible)
npx playwright test --headed

# Exécuter un fichier de test spécifique
npx playwright test login.spec.ts

# Exécuter tests avec pattern
npx playwright test auth

# Mode debug interactif
npx playwright test --debug

# Mode debug sur test spécifique
npx playwright test login.spec.ts --debug
```

#### Options de Navigateur
```bash
# Chromium uniquement (défaut)
npx playwright test --project=chromium

# Firefox uniquement
npx playwright test --project=firefox

# WebKit (Safari) uniquement
npx playwright test --project=webkit

# Tous les navigateurs
npx playwright test --project=chromium --project=firefox --project=webkit
```

#### Rapports et Résultats
```bash
# Générer rapport HTML
npx playwright test --reporter=html

# Voir le dernier rapport
npx playwright show-report

# Reporter JSON
npx playwright test --reporter=json

# Reporter détaillé en ligne de commande
npx playwright test --reporter=list

# Reporter avec screenshots
npx playwright test --screenshot=on

# Capturer vidéo des tests
npx playwright test --video=on
```

#### Traces et Débogage
```bash
# Enregistrer traces pour analyse
npx playwright test --trace=on

# Voir les traces
npx playwright show-trace trace.zip

# Mode pas-à-pas
npx playwright test --debug

# Inspector Playwright (UI de debug)
PWDEBUG=1 npx playwright test
```

#### Parallélisation et Performance
```bash
# Exécuter en parallèle (par défaut)
npx playwright test

# Limiter workers
npx playwright test --workers=2

# Mode séquentiel (un test à la fois)
npx playwright test --workers=1

# Retry sur échec
npx playwright test --retries=2

# Timeout personnalisé
npx playwright test --timeout=60000
```

#### Filtrage et Sélection
```bash
# Exécuter tests contenant "login"
npx playwright test -g "login"

# Exécuter tests sauf ceux contenant "slow"
npx playwright test --grep-invert "slow"

# Tests par tag
npx playwright test --grep @smoke

# Tests modifiés uniquement (avec git)
npx playwright test --only-changed
```

#### Configuration et Environnement
```bash
# Utiliser configuration spécifique
npx playwright test --config=playwright.prod.config.ts

# Variables d'environnement
BASE_URL=http://localhost:4200 npx playwright test

# Mode CI (plus rapide, moins verbeux)
CI=1 npx playwright test
```

#### Génération de Code
```bash
# Codegen - Enregistrer actions en code
npx playwright codegen http://localhost:4200

# Codegen avec authentification
npx playwright codegen --save-storage=auth.json http://localhost:4200

# Codegen avec device émulé
npx playwright codegen --device="iPhone 13" http://localhost:4200
```

#### Scripts package.json Recommandés
```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:chromium": "playwright test --project=chromium",
    "test:e2e:firefox": "playwright test --project=firefox",
    "test:e2e:webkit": "playwright test --project=webkit",
    "test:e2e:report": "playwright show-report",
    "test:e2e:trace": "playwright show-trace",
    "test:e2e:codegen": "playwright codegen http://localhost:4200"
  }
}
```

#### Configuration playwright.config.ts
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:4200',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:4200',
    reuseExistingServer: !process.env.CI,
  },
});
```

#### Exemples de Tests Avancés
```typescript
// Test avec authentification réutilisable
test.use({ storageState: 'auth.json' });

test('profile access', async ({ page }) => {
  await page.goto('/profile');
  await expect(page).toHaveURL(/.*profile/);
});

// Test avec mocking API
test('mock API response', async ({ page }) => {
  await page.route('**/api/posts', route => 
    route.fulfill({
      status: 200,
      body: JSON.stringify([{ id: 1, title: 'Test' }])
    })
  );
  await page.goto('/my-posts');
});

// Test responsive
test('mobile view', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');
});
```

### 5.4.2 Tests API (Postman)

Collection Postman créée avec :
- ✅ Tous les 14 endpoints
- ✅ Tests assertions (status 200, structure JSON)
- ✅ Variables d'environnement (token)
- ✅ Pre-request scripts pour auth

## 5.5 Déploiement

### 5.5.1 Docker Compose

**docker-compose.yml** :
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: redditdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - kafka
    environment:
      DATABASE_URL: postgresql://postgres:123@postgres:5432/redditdb

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### 5.5.2 Commandes de Déploiement

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f backend

# Scaler le backend
docker-compose up -d --scale backend=3

# Arrêter
docker-compose down

# Arrêter + supprimer volumes
docker-compose down -v
```

## 5.6 Difficultés Rencontrées et Solutions

| Difficulté | Solution Apportée |
|------------|-------------------|
| **Rate limiting Reddit API** | Cache des résultats, limitation à 20 posts |
| **CORS errors** | Configuration CORS explicite dans FastAPI |
| **WebSocket disconnections** | Reconnexion automatique côté client |
| **Duplicate notifications** | Contrainte UNIQUE(user_id, content) |
| **Performance analytics** | Indexes sur colonnes fréquemment requêtées |
| **Token expiration** | Refresh automatique ou redirect login |
| **Docker networking** | Utilisation de noms de services Docker |

## 5.7 Métriques du Projet

| Métrique | Valeur |
|----------|--------|
| **Lignes de code Backend** | ~2500 |
| **Lignes de code Frontend** | ~3000 |
| **Nombre de composants Angular** | 7 |
| **Nombre d'endpoints API** | 14 REST + 1 WebSocket |
| **Nombre de tables DB** | 7 |
| **Temps de développement** | 2 mois |
| **Couverture tests E2E** | Login, Register, Subscribe |
| **Temps moyen réponse API** | < 150ms |
| **Taille image Docker backend** | ~800MB |
| **Taille image Docker frontend** | ~150MB |
