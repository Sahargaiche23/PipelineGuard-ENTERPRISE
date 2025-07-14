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

def get_post_level(score):
    if score >= 1000:
        return "top"
    elif score >= 100:
        return "moyen"
    else:
        return "bas"

# Stream des nouveaux posts du subreddit
for post in subreddit.stream.submissions():
    level = get_post_level(post.score)
    data = {
        'id': post.id,
        'title': post.title,
        'author': str(post.author) if post.author else "unknown",
        'created_utc': float(post.created_utc),
        'url': post.url,
        'score': post.score,
        'level': level,
        'query': subreddit_name
    }
    print(f"📤 Sending post: {data['title']} [score={data['score']}, niveau={data['level']}]")
    producer.send("reddit_posts", data)
    producer.flush()  # Force l'envoi du message tout de suite (optionnel)