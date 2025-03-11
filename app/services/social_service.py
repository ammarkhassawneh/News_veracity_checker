import os
import tweepy
import instaloader
from datetime import datetime

def analyze_twitter(keyword: str) -> tuple:
    """
    Performs advanced analysis of Twitter data for a given keyword.
    
    It fetches recent tweets containing the keyword, extracts timeline events,
    and computes a veracity score based on the proportion of tweets from verified users.
    
    Returns:
        tuple: (veracity_score (float), report (str))
    """
    # Retrieve Twitter API credentials from environment variables
    twitter_api_key = os.getenv("TWITTER_API_KEY")
    twitter_api_secret = os.getenv("TWITTER_API_SECRET")
    twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    if not all([twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_token_secret]):
        return 0.0, "Twitter API credentials not provided."
    
    try:
        # Authenticate with Twitter API using OAuth1
        auth = tweepy.OAuth1UserHandler(
            twitter_api_key, twitter_api_secret,
            twitter_access_token, twitter_access_token_secret
        )
        api = tweepy.API(auth)
        
        # Fetch recent tweets containing the keyword (up to 100 tweets)
        tweets = api.search_tweets(q=keyword, lang="en", count=100, tweet_mode="extended")
        total_tweets = len(tweets)
        verified_tweets = [tweet for tweet in tweets if tweet.user.verified]
        
        # Build timeline events from tweets
        timeline = []
        for tweet in tweets:
            timeline.append({
                "username": tweet.user.screen_name,
                "date": tweet.created_at.isoformat(),
                "text": tweet.full_text
            })
        
        score = len(verified_tweets) / total_tweets if total_tweets > 0 else 0.0
        report = f"Twitter analysis: Found {total_tweets} tweets for keyword '{keyword}'.\n"
        report += f"Verified tweets: {len(verified_tweets)}. Calculated veracity score: {score:.2f}.\n"
        report += "Timeline:\n"
        for event in timeline:
            report += f"{event['date']} - {event['username']}: {event['text']}\n"
        return score, report
    except Exception as e:
        return 0.0, f"Twitter analysis error: {str(e)}"

def analyze_facebook(keyword: str) -> tuple:
    """
    Performs advanced analysis of Facebook data for a given keyword.
    
    This function simulates fetching and analyzing Facebook posts containing the keyword,
    and generates a timeline of events from reputable sources.
    
    Returns:
        tuple: (veracity_score (float), report (str))
    """
    facebook_api_key = os.getenv("FACEBOOK_API_KEY")
    if not facebook_api_key:
        return 0.0, "Facebook API credentials not provided."
    
    try:
        # Placeholder: In a real scenario, use the facebook-sdk to query Facebook's Graph API.
        # Simulated timeline data from trusted sources:
        timeline = [
            {"source": "Reuters", "date": "2025-03-10T12:00:00", "text": f"{keyword} breaking news from Reuters."},
            {"source": "AP", "date": "2025-03-10T12:05:00", "text": f"{keyword} update from AP."},
            {"source": "BBC", "date": "2025-03-10T12:10:00", "text": f"{keyword} report from BBC."}
        ]
        score = 0.75  # Dummy score based on simulated analysis
        report = f"Facebook analysis: Simulated timeline for keyword '{keyword}'.\nTimeline:\n"
        for event in timeline:
            report += f"{event['date']} - {event['source']}: {event['text']}\n"
        report += f"Calculated veracity score: {score:.2f}."
        return score, report
    except Exception as e:
        return 0.0, f"Facebook analysis error: {str(e)}"

def analyze_instagram(keyword: str) -> tuple:
    """
    Performs advanced analysis of Instagram data for a given hashtag.
    
    It uses Instaloader to fetch posts under the given hashtag,
    builds a timeline of recent posts, and computes a veracity score.
    
    Returns:
        tuple: (veracity_score (float), report (str))
    """
    try:
        loader = instaloader.Instaloader()
        hashtag = instaloader.Hashtag.from_name(loader.context, keyword)
        posts = hashtag.get_posts()
        timeline = []
        count = 0
        for post in posts:
            timeline.append({
                "username": post.owner_username,
                "date": post.date_utc.isoformat(),
                "caption": post.caption if post.caption else ""
            })
            count += 1
            if count >= 20:
                break
        # Dummy logic: Higher number of posts suggests wider discussion and thus a moderately higher score.
        score = 0.65 if count > 10 else 0.45
        report = f"Instagram analysis: Analyzed {count} posts for hashtag '{keyword}'.\nTimeline:\n"
        for event in timeline:
            report += f"{event['date']} - {event['username']}: {event['caption']}\n"
        report += f"Calculated veracity score: {score:.2f}."
        return score, report
    except Exception as e:
        return 0.0, f"Instagram analysis error: {str(e)}"
