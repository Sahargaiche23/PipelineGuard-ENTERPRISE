import praw
from kafka import KafkaProducer
import json
from config import REDDIT_CONFIG

# Initialisation de l'API Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CONFIG['client_id'],
    client_secret=REDDIT_CONFIG['client_secret'],
    username=REDDIT_CONFIG['username'],
    password=REDDIT_CONFIG['password'],
    user_agent=REDDIT_CONFIG['user_agent']
)

# Initialisation du Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

subreddit = reddit.subreddit("technology")

# Stream des nouveaux posts du subreddit
for post in subreddit.stream.submissions():
    data = {
        'id': post.id,
        'title': post.title,
        'author': str(post.author) if post.author else "unknown",
        'created_utc': float(post.created_utc),
        'url': post.url
    }
    print(f"📤 Sending post: {data['title']}")
    producer.send("reddit_posts", data)
    producer.flush()  # Force l'envoi du message tout de suite (optionnel)