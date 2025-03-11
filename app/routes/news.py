import os
import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import News

# Import advanced analysis functions from services
from app.services.nlp_service import analyze_text
from app.services.media_service import analyze_image, analyze_video
from app.services.social_service import analyze_twitter, analyze_facebook, analyze_instagram
from app.services.scraper import scrape_headlines

router = APIRouter()

@router.post("/verify", summary="Verify the veracity of news", response_model=dict)
async def verify_news(
    input_type: str = Form(...),         # Expected values: "text", "link", "image", "video"
    input_data: str = Form(None),          # For text or link input (a single field for both)
    file: UploadFile = File(None),         # For image or video input
    db: Session = Depends(get_db)
):
    """
    This endpoint processes the user input (which can be text, link, image, or video)
    and performs advanced veracity analysis. It integrates:
      - Primary analysis based on the input content (text analysis, media analysis, or scraping for links).
      - Social media analysis from Twitter, Facebook, and Instagram.
      - Aggregates the results into a final veracity score and detailed report.

    Input requirements:
      - For "text" or "link": only the 'input_data' field is required.
      - For "image" or "video": only the file upload is required.
    """
    primary_report = {}

    if input_type.lower() == "text":
        if not input_data:
            raise HTTPException(status_code=400, detail="Text content is required for text input.")
        score, report = analyze_text(input_data)
        primary_report = {"veracity_score": score, "analysis_report": report}

    elif input_type.lower() == "link":
        if not input_data:
            raise HTTPException(status_code=400, detail="URL is required for link input.")
        # Scrape the link to extract headlines (as a proxy for article content)
        headlines = scrape_headlines(input_data)
        if not headlines:
            raise HTTPException(status_code=400, detail="Could not extract content from the provided URL.")
        combined_text = " ".join(headlines)
        score, report = analyze_text(combined_text)
        primary_report = {
            "veracity_score": score,
            "analysis_report": report,
            "extracted_headlines": headlines
        }

    elif input_type.lower() == "image":
        if file is None:
            raise HTTPException(status_code=400, detail="Image file is required for image input.")
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        score, report = analyze_image(file_location)
        primary_report = {"veracity_score": score, "analysis_report": report}
        os.remove(file_location)

    elif input_type.lower() == "video":
        if file is None:
            raise HTTPException(status_code=400, detail="Video file is required for video input.")
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        score, report = analyze_video(file_location)
        primary_report = {"veracity_score": score, "analysis_report": report}
        os.remove(file_location)

    else:
        raise HTTPException(status_code=400, detail="Invalid input type provided.")

    # Social media analysis integration:
    # Use a snippet from the input_data (if available) or default keyword for social media search.
    social_keyword = input_data.split()[0] if input_data else "news"
    twitter_score, twitter_report = analyze_twitter(social_keyword)
    facebook_score, facebook_report = analyze_facebook(social_keyword)
    instagram_score, instagram_report = analyze_instagram(social_keyword)

    social_media = {
        "twitter": {"score": twitter_score, "report": twitter_report},
        "facebook": {"score": facebook_score, "report": facebook_report},
        "instagram": {"score": instagram_score, "report": instagram_report}
    }

    # Calculate a weighted final veracity score:
    # Primary analysis weight: 60%, Social media analysis weight: 40%
    social_avg = (twitter_score + facebook_score + instagram_score) / 3
    final_score = 0.6 * primary_report["veracity_score"] + 0.4 * social_avg

    # Prepare the final integrated report
    final_report = {
        "input_type": input_type,
        "primary_analysis": primary_report,
        "social_media_analysis": social_media,
        "final_veracity_score": final_score,
        "conclusion": "News is likely authentic." if final_score > 0.5 else "News is likely fake."
    }

    # Optionally, save the record to the database for text and link inputs
    if input_type.lower() in ["text", "link"]:
        new_news = News(
            title=input_data if input_data else (file.filename if file else "Media Analysis"),
            content=input_data if input_data else "Media file analysis",
            source=input_data if input_type.lower() == "link" else "User Submitted",
            published_date=datetime.datetime.utcnow(),
            veracity_score=final_score,
            is_fake=(final_score < 0.5),
            analysis_report=str(final_report)
        )
        db.add(new_news)
        db.commit()
        db.refresh(new_news)
        final_report["news_record_id"] = new_news.id

    return final_report
