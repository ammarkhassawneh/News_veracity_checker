from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import News
from app.services.nlp_service import analyze_text

# Define a Pydantic model for the input data
class NewsInput(BaseModel):
    title: str      # The title of the news article
    content: str    # The full content of the news article
    source: str = None  # Optional source of the news article

# Create an API router for news-related endpoints
router = APIRouter()

@router.post("/verify", summary="Verify the veracity of news", response_model=dict)
def verify_news(news_input: NewsInput, db: Session = Depends(get_db)):
    """
    Endpoint to verify the veracity of a news article.
    It accepts a JSON payload with the title, content, and optional source.
    The content is analyzed using the NLP service to determine a veracity score and generate an analysis report.
    The news article is then stored in the database.
    """
    # Validate input data: title and content are required
    if not news_input.title or not news_input.content:
        raise HTTPException(status_code=400, detail="Title and content are required")
    
    # Analyze the news content using the NLP service (dummy analysis for MVP)
    veracity_score, analysis_report = analyze_text(news_input.content)
    
    # Create a new News record
    new_news = News(
        title=news_input.title,
        content=news_input.content,
        source=news_input.source or "Unknown",
        veracity_score=veracity_score,
        is_fake=(veracity_score < 0.5),  # Mark as fake if score is below 0.5
        analysis_report=analysis_report
    )
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    
    # Return the result as a JSON response
    return {
        "id": new_news.id,
        "veracity_score": new_news.veracity_score,
        "is_fake": new_news.is_fake,
        "analysis_report": new_news.analysis_report
    }
