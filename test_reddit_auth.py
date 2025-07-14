import praw
from config import REDDIT_CONFIG

reddit = praw.Reddit(
    client_id=REDDIT_CONFIG['client_id'],
    client_secret=REDDIT_CONFIG['client_secret'],
    username=REDDIT_CONFIG['username'],
    password=REDDIT_CONFIG['password'],
    user_agent=REDDIT_CONFIG['user_agent']
)

try:
    user = reddit.user.me()
    print(f"✅ Authentification réussie en tant que : {user}")
except Exception as e:
    print(f"❌ Échec de l'authentification : {e}")
