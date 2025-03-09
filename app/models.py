from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Define the base class for SQLAlchemy models
Base = declarative_base()

class News(Base):
    __tablename__ = "news"

    # Unique identifier for each news entry
    id = Column(Integer, primary_key=True, index=True)
    
    # Title of the news article
    title = Column(String(256), nullable=False)
    
    # Full content of the news article
    content = Column(Text, nullable=False)
    
    # Source URL or name of the news article
    source = Column(String(256), nullable=True)
    
    # Date and time when the news was published or added
    published_date = Column(DateTime, default=datetime.utcnow)
    
    # Score indicating the veracity of the news (e.g., percentage or other metric)
    veracity_score = Column(Float, nullable=True)
    
    # Flag indicating whether the news is considered fake
    is_fake = Column(Boolean, default=False)
    
    # Detailed analysis report about the news veracity
    analysis_report = Column(Text, nullable=True)
