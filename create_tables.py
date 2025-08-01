from database import Base, engine
from models import RedditPost
from models import Subscription

Base.metadata.create_all(bind=engine)