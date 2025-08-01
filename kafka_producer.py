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

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

subreddit_name = "technology"
subreddit = reddit.subreddit(subreddit_name)

# ----------- Filtre personnalisé -----------
# Par exemple, on ne garde que les posts dont le titre contient "AI"
def custom_filter(post):
    return "AI" in post.title or "ai" in post.title

# Stream des nouveaux posts du subreddit
for post in subreddit.stream.submissions():
    if custom_filter(post):  # <-- Ici tu mets ta logique de filtre
        data = {
            'id': post.id,
            'title': post.title,
            'author': str(post.author) if post.author else "unknown",
            'created_utc': float(post.created_utc),
            'url': post.url,
            'score': post.score,
            'query': subreddit_name
        }
        print(f"📤 Sending post: {data['title']}")
        producer.send("reddit_posts", data)
        producer.flush()