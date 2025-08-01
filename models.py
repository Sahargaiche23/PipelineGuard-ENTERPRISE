from sqlalchemy import Column, Integer, String, DateTime, Float, UniqueConstraint
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint('user_id', 'content', name='_user_content_uc'),)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    topic = Column(String)      # nom du subreddit
    level = Column(String)      # "top", "moyen", "bas"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
class RedditPost(Base):
    __tablename__ = "reddit_posts"
    id = Column(String, primary_key=True, index=True)  # <-- clé primaire obligatoire
    title = Column(String)
    author = Column(String)
    created_utc = Column(Float)
    url = Column(String)
    score = Column(Integer)
    level = Column(String)
    topic = Column(String)
    created_at = Column(DateTime)