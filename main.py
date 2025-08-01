import asyncio
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import praw
from auth import router as auth_router, get_current_user
from config import REDDIT_CONFIG
from websocket_manager import manager
from jose import jwt, JWTError
from models import Notification, User, Subscription
from database import SessionLocal
from sqlalchemy.exc import IntegrityError
import json

app = FastAPI()

# CORS pour Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes d'authentification
app.include_router(auth_router)

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    username = None
    db = None
    try:
        await websocket.accept()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        await manager.connect(username, websocket)
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        if not user:
            await websocket.close()
            return
        user_id = user.id
        seen = set()
        notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
        for notif in notifications:
            message = {
                "id": notif.id,
                "title": "Notification Reddit",
                "content": notif.content or "",
                "url": "",
                "created_at": str(notif.created_at) if notif.created_at else ""
            }
            await websocket.send_text(json.dumps(message))
            seen.add(notif.id)
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
                    seen.add(notif.id)
    except JWTError:
        try:
            await websocket.close()
        except:
            pass
    except Exception:
        try:
            await websocket.close()
        except:
            pass
    finally:
        if db:
            db.close()
        if username:
            manager.disconnect(username)

@app.get("/notifications")
async def get_notifications(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
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
        return result
    finally:
        db.close()

@app.delete("/notifications")
async def clear_notifications(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        deleted_count = db.query(Notification).filter(Notification.user_id == current_user.id).delete()
        db.commit()
        return {"message": f"{deleted_count} notifications supprimées avec succès"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression des notifications")
    finally:
        db.close()

@app.get("/search")
async def search_posts(
    q: str,
    current_user: User = Depends(get_current_user)
):
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
                "level": level,
                "url": post.url,
                "author": str(post.author) if post.author else "unknown",
                "created_utc": float(post.created_utc)
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la recherche Reddit")

@app.post("/subscribe")
async def subscribe(
    topic: str,
    level: str,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        existing = db.query(Subscription).filter_by(
            user_id=current_user.id, topic=topic, level=level
        ).first()
        if existing:
            return {"message": "Déjà abonné à ce topic/niveau"}
        sub = Subscription(user_id=current_user.id, topic=topic, level=level)
        db.add(sub)
        # --- Ajout d'une notification ---
        notif = Notification(
            user_id=current_user.id,
            content=f"Abonnement au topic '{topic}' niveau '{level}'"
        )
        db.add(notif)
        db.commit()
        return {"message": "Abonnement enregistré et notification créée"}
    except IntegrityError:
        db.rollback()
        return {"message": "Erreur d'intégrité"}
    finally:
        db.close()

@app.get("/my_posts")
async def get_my_posts(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        subs = db.query(Subscription).filter_by(user_id=current_user.id).all()
        results = []
        reddit = praw.Reddit(
            client_id=REDDIT_CONFIG['client_id'],
            client_secret=REDDIT_CONFIG['client_secret'],
            username=REDDIT_CONFIG['username'],
            password=REDDIT_CONFIG['password'],
            user_agent=REDDIT_CONFIG['user_agent']
        )
        for sub in subs:
            subreddit = reddit.subreddit(sub.topic)
            for post in subreddit.hot(limit=20):
                # On ne regarde plus le score, on garde le level de l'abonnement
                if not any(p["id"] == post.id for p in results):
                    results.append({
                        "id": post.id,
                        "title": post.title,
                        "level": sub.level,  # le level choisi à l'abonnement
                        "url": post.url,
                        "author": str(post.author) if post.author else "unknown",
                        "created_utc": float(post.created_utc),
                        "topic": sub.topic
                    })
        return results
    finally:
        db.close()
    db = SessionLocal()
    try:
        subs = db.query(Subscription).filter_by(user_id=current_user.id).all()
        results = []
        reddit = praw.Reddit(
            client_id=REDDIT_CONFIG['client_id'],
            client_secret=REDDIT_CONFIG['client_secret'],
            username=REDDIT_CONFIG['username'],
            password=REDDIT_CONFIG['password'],
            user_agent=REDDIT_CONFIG['user_agent']
        )
        for sub in subs:
            subreddit = reddit.subreddit(sub.topic)
            for post in subreddit.hot(limit=20):
                level = "top" if post.score >= 1000 else "moyen" if post.score >= 100 else "bas"
                if level == sub.level:
                    if not any(p["id"] == post.id for p in results):
                        results.append({
                            "id": post.id,
                            "title": post.title,
                            "score": post.score,
                            "level": level,
                            "url": post.url,
                            "author": str(post.author) if post.author else "unknown",
                            "created_utc": float(post.created_utc),
                            "topic": sub.topic
                        })
        return results
    finally:
        db.close()