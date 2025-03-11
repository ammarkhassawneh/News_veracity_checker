# News Veracity Checker

## Overview
News Veracity Checker is an AI-based tool designed to verify the authenticity of news. It accepts input in the form of text, URLs, images, or videos and analyzes them using advanced AI techniques. The tool provides a detailed report on the veracity of the news article.

## Features
- **Multimodal Input Support**: Accepts text, URLs, images, and videos.
- **Advanced NLP Analysis**: Utilizes state-of-the-art models (e.g., Facebook's BART-large-MNLI for zero-shot classification) for robust text analysis.
- **Media Analysis**: Analyzes images and videos using deep learning-inspired techniques.
- **Social Media Analysis**: Integrates with Twitter, Facebook, and Instagram to fetch and analyze social media data.
- **Trusted Sources Comparison**: Compares news content against a wide range of reliable sources such as BBC, CNN, Al Jazeera, Google News, Reuters, AP, and The Guardian.
- **Database Storage**: Stores analyzed news articles in a database (SQLite by default) using SQLAlchemy.
- **API with FastAPI**: Provides a scalable and high-performance API built using FastAPI.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:ammarkhassawneh/News_veracity_checker.git
   cd News_veracity_checker

    Create and Activate a Virtual Environment:

python3 -m venv fack
source fack/bin/activate

Install the Dependencies:

pip install -r requirements.txt

Set Up Environment Variables: Create a .env file in the project root directory and add your API keys and other configuration variables:

    DATABASE_URL=sqlite:///./news.db
    NLP_MODEL_NAME=bert-base-uncased
    TWITTER_API_KEY=your_twitter_api_key
    TWITTER_API_SECRET=your_twitter_api_secret
    TWITTER_ACCESS_TOKEN=your_twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
    FACEBOOK_API_KEY=your_facebook_api_key
    INSTAGRAM_API_KEY=your_instagram_api_key
    DEBUG_MODE=True

Running the Application

Start the FastAPI application using Uvicorn:

uvicorn app.main:app --reload

The API will be available at http://localhost:8000.
Testing

Run tests using pytest:

pytest

Project Structure

news_veracity_checker/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── database.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── news.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── nlp_service.py
│   │   ├── media_service.py
│   │   ├── social_service.py
│   │   └── scraper.py
│   └── utils/
│       ├── __init__.py
│       └── helper.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
└── README.md