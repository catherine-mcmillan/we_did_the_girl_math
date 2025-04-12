from app import create_app, db
from app.models.user import User
from app.models.post import Post, Vote, Comment

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    
    print("Database tables created successfully!") 