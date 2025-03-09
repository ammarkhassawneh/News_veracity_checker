from fastapi import FastAPI
from app.routes.news import router as news_router

# Create a FastAPI instance
app = FastAPI(
    title="News Veracity Checker",
    description="AI tool to verify fake news using various services.",
    version="0.1.0"
)

# Include the news router
app.include_router(news_router, prefix="/news", tags=["News"])

if __name__ == "__main__":
    import uvicorn
    # Run the application using uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000)
