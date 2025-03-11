from app.database import engine
from app.models import Base

# Create all tables defined in the models
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")
