from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.db.base import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and "supabase.co" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"options": "-c default_transaction_isolation=read_committed"})
else:
    engine = create_engine(DATABASE_URL, echo=True)  

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.models import ticket, category, user, ticket_analytics

def init_db():
    """
    Initialize the database by creating all tables defined in the models
    """
    try:
        with engine.connect() as conn:
            print("Database connection successful!")
        
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print(f"DATABASE_URL: {DATABASE_URL}")
        print("Please check your database connection and try again.")
        return False
    
    return True
    


if __name__ == "__main__":
    init_db()


