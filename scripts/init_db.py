from flask import Flask
from flask_migrate import Migrate
from app import create_app
from app.models.database import db

def init_db():
    """Initialize the database with required tables"""
    app = create_app()
    
    with app.app_context():
        # Initialize migrations
        Migrate(app, db)
        
        # Create all tables
        db.create_all()
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 