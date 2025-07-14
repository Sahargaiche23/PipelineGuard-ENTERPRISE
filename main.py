import asyncio
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import praw
from auth import router as auth_router, get_current_user
from config import REDDIT_CONFIG
from websocket_manager import manager
from jose import jwt, JWTError
from models import Notification, User
from database import SessionLocal
import json

# ✅ Crée l'application une seule fois
app = FastAPI()

# ✅ CORS pour Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Inclure les routes d'authentification
app.include_router(auth_router)

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    username = None
    db = None
    try:
        print(f"🔌 Nouvelle connexion WebSocket avec token: {token[:20]}...")
        
        # Accepter la connexion WebSocket en premier
        await websocket.accept()
        print(f"✅ Connexion WebSocket acceptée")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        print(f"✅ Token décodé avec succès, utilisateur: {username}")
        
        await manager.connect(username, websocket)
        print(f"✅ Connexion WebSocket établie pour {username}")

        db = SessionLocal()
        
        # Debug: Liste tous les utilisateurs
        all_users = db.query(User).all()
        print(f"👥 Utilisateurs disponibles: {[u.username for u in all_users]}")
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"❌ Utilisateur {username} non trouvé dans la base de données")
            await websocket.close()
            return
        user_id = user.id
        print(f"✅ Utilisateur trouvé avec ID: {user_id}")

        # Debug: Compter toutes les notifications
        all_notifications = db.query(Notification).all()
        user_notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
        print(f"📬 Total notifications dans DB: {len(all_notifications)}")
        print(f"📬 Notifications pour {username}: {len(user_notifications)}")

        seen = set()
        # Envoyer toutes les notifications existantes d'abord
        notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
        print(f"📤 Envoi de {len(notifications)} notifications existantes...")
        
        for notif in notifications:
            message = {
                "id": notif.id,
                "title": "Notification Reddit",
                "content": notif.content or "",
                "url": "",
                "created_at": str(notif.created_at) if notif.created_at else ""
            }
            await websocket.send_text(json.dumps(message))
            print(f"📤 Notification envoyée: {message}")
            seen.add(notif.id)
        
        # Puis surveiller les nouvelles notifications
        while True:
            await asyncio.sleep(5)
            new_notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
            for notif in new_notifications:
                if notif.id not in seen:
                    message = {
                        "id": notif.id,
                        "title": "Notification Reddit",
                        "content": notif.content or "",
                        "url": "",
                        "created_at": str(notif.created_at) if notif.created_at else ""
                    }
                    await websocket.send_text(json.dumps(message))
                    print(f"📤 Nouvelle notification envoyée: {message}")
                    seen.add(notif.id)
    except JWTError as e:
        print(f"❌ Erreur JWT: {e}")
        try:
            await websocket.close()
        except:
            pass
    except Exception as e:
        print(f"❌ Erreur WebSocket: {e}")
        import traceback
        traceback.print_exc()
        try:
            await websocket.close()
        except:
            pass
    finally:
        if db:
            db.close()
        if username:
            print(f"🔌 Déconnexion WebSocket pour {username}")
            manager.disconnect(username)

@app.get("/notifications")
async def get_notifications(current_user: User = Depends(get_current_user)):
    """Récupère les notifications de l'utilisateur connecté depuis la base de données"""
    db = SessionLocal()
    try:
        print(f"📋 Récupération des notifications pour {current_user.username}")
        
        # Récupérer toutes les notifications de l'utilisateur
        notifications = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
        
        result = []
        for notif in notifications:
            result.append({
                "id": notif.id,
                "title": "Notification Reddit",
                "content": notif.content or "",
                "url": "",
                "created_at": str(notif.created_at) if notif.created_at else ""
            })
        
        print(f"✅ {len(result)} notifications trouvées pour {current_user.username}")
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des notifications: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des notifications")
    finally:
        db.close()

@app.delete("/notifications")
async def clear_notifications(current_user: User = Depends(get_current_user)):
    """Supprime toutes les notifications de l'utilisateur connecté"""
    db = SessionLocal()
    try:
        print(f"🧹 Suppression des notifications pour {current_user.username}")
        
        # Supprimer toutes les notifications de l'utilisateur
        deleted_count = db.query(Notification).filter(Notification.user_id == current_user.id).delete()
        db.commit()
        
        print(f"✅ {deleted_count} notifications supprimées pour {current_user.username}")
        return {"message": f"{deleted_count} notifications supprimées avec succès"}
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression des notifications: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression des notifications")
    finally:
        db.close()
@app.get("/search")
async def search_posts(q: str):
    """
    Recherche des posts Reddit par sujet (subreddit ou mot-clé).
    Retourne les posts avec leur score et niveau (top/moyen/bas).
    """
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CONFIG['client_id'],
            client_secret=REDDIT_CONFIG['client_secret'],
            username=REDDIT_CONFIG['username'],
            password=REDDIT_CONFIG['password'],
            user_agent=REDDIT_CONFIG['user_agent']
        )
        subreddit = reddit.subreddit(q)
        results = []
        for post in subreddit.hot(limit=20):
            level = "top" if post.score >= 1000 else "moyen" if post.score >= 100 else "bas"
            results.append({
                "id": post.id,
                "title": post.title,
                "score": post.score,
                "level": level,
                "url": post.url,
                "author": str(post.author) if post.author else "unknown",
                "created_utc": float(post.created_utc)
            })
        return results
    except Exception as e:
        print(f"❌ Erreur lors de la recherche Reddit: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la recherche Reddit")