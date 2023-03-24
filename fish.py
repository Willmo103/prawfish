from praw import Reddit
from config import settings


def _create_client():
reddit = Reddit(client_id=settings.client_id,
                client_secret=settings.client_secret,
                user_agent=settings.user_agent)
