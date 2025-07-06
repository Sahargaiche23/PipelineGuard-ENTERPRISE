import praw
from kafka import KafkaProducer
import json
from config import REDDIT_CONFIG

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

subreddit = reddit.subreddit("technology")

for post in subreddit.stream.submissions():
    data = {
        'id': post.id,
        'title': post.title,
        'author': str(post.author),
        'created_utc': post.created_utc,
        'url': post.url
    }
    print(f"📤 Sending post: {data['title']}")
    producer.send("reddit_posts", data)
