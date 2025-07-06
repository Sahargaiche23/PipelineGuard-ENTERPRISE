from kafka import KafkaConsumer
import psycopg2
import json
import time

# 🔁 Connexion au consumer Kafka
consumer = KafkaConsumer(
    'reddit_posts',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',   # Commencer depuis le début si aucune position enregistrée
    enable_auto_commit=True
)

# 🔐 Connexion à la base PostgreSQL/TimescaleDB
try:
    conn = psycopg2.connect(
        dbname='redditdb',
        user='postgres',
        password='123',       # Ton mot de passe ici
        host='localhost',
        port=5433             # Ton conteneur PostgreSQL écoute ici
    )
    cur = conn.cursor()
    print("✅ Connexion à la base de données réussie.")
except Exception as e:
    print("❌ Erreur de connexion à la base de données :", e)
    exit(1)

# 📥 Lecture des messages Kafka et insertion en base
try:
    for msg in consumer:
        data = msg.value
        print("📥 Reçu :", data)

        try:
            cur.execute(
                "INSERT INTO reddit_posts (title, created_at) VALUES (%s, to_timestamp(%s))",
                (data['title'], data['created_utc'])
            )
            conn.commit()
            print(f"✅ Post inséré : {data['title']}")
        except Exception as insert_error:
            print(f"❌ Erreur insertion : {insert_error}")
            conn.rollback()

except KeyboardInterrupt:
    print("\n🛑 Arrêt manuel du consumer.")
finally:
    cur.close()
    conn.close()
    print("🔒 Connexion PostgreSQL fermée.")
