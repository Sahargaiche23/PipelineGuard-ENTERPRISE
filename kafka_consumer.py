from kafka import KafkaConsumer
import psycopg2
import json
from websocket_manager import manager  # Optionnel, seulement si FastAPI tourne et manager actif
from models import Notification, User
from database import SessionLocal
import asyncio

# --- Connexion Kafka ---
consumer = KafkaConsumer(
    'reddit_posts',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# --- Connexion psycopg2 pour reddit_posts ---
try:
    conn = psycopg2.connect(
        dbname='redditdb',
        user='postgres',
        password='123',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()
    print("✅ Connexion à la base de données réussie (psycopg2).")
except Exception as e:
    print("❌ Erreur de connexion à la base de données :", e)
    exit(1)

# --- Fonction d'insertion notifications (SQLAlchemy) et posts (psycopg2) ---
async def handle_message():
    db = SessionLocal()
    try:
        for msg in consumer:
            data = msg.value
            print("📥 Reçu :", data)

            # Insertion dans reddit_posts (psycopg2)
            try:
                cur.execute(
                    "INSERT INTO reddit_posts (title, created_at) VALUES (%s, to_timestamp(%s))",
                    (data['title'], data['created_utc'])
                )
                conn.commit()
                print(f"✅ Post inséré : {data['title']}")
            except Exception as insert_error:
                print(f"❌ Erreur insertion reddit_posts : {insert_error}")
                conn.rollback()

            # Insertion dans notifications (SQLAlchemy) pour chaque utilisateur
            users = db.query(User).all()
            for user in users:
                exists = db.query(Notification).filter_by(user_id=user.id, content=data["title"]).first()
                if exists:
                    print(f"⏩ Notification déjà présente pour {user.username}")
                    continue
                notif = Notification(
                    user_id=user.id,
                    content=data["title"]
                )
                db.add(notif)
                db.commit()
                print(f"✅ Notification insérée pour {user.username}")

                # (Optionnel) Envoi en temps réel si le user est connecté via WebSocket
                try:
                    await manager.send_personal_message(f"🔔 {data['title']}", user.username)
                except Exception:
                    pass  # Si le manager n'est pas dispo, on ignore
    except KeyboardInterrupt:
        print("\n🛑 Arrêt manuel du consumer.")
    finally:
        db.close()
        cur.close()
        conn.close()
        print("🔒 Connexions fermées.")

if __name__ == "__main__":
    asyncio.run(handle_message())