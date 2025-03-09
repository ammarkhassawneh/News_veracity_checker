import os

# This file contains configuration settings for the application.

# Database configuration: sets the database URL, defaulting to a SQLite database if not provided via environment variables.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news.db")

# Trusted news sources: an expanded list of reliable news websites for comparison.
TRUSTED_SOURCES = [
    "https://www.bbc.com",         # BBC News
    "https://www.cnn.com",         # CNN
    "https://www.aljazeera.com",   # Al Jazeera
    "https://news.google.com",     # Google News
    "https://www.reuters.com",     # Reuters
    "https://apnews.com",          # Associated Press
    "https://www.theguardian.com"  # The Guardian
]

# NLP Model configuration: specifies the name of the NLP model to be used, defaulting to a BERT model.
NLP_MODEL_NAME = os.getenv("NLP_MODEL_NAME", "bert-base-uncased")

# API keys for social media platforms (placeholders); these should be set in the environment for production.
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
FACEBOOK_API_KEY = os.getenv("FACEBOOK_API_KEY", "")
INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY", "")

# Other configurations: a flag to indicate if the application should run in debug mode.
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() in ["true", "1", "t"]
