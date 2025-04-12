from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    expense = db.Column(db.String(200), nullable=False)
    justification = db.Column(db.Text, nullable=False)
    is_seeking_help = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    votes = db.relationship('Vote', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def vote_count(self, vote_type=None):
        if vote_type:
            return Vote.query.filter_by(post_id=self.id, vote_type=vote_type).count()
        return Vote.query.filter_by(post_id=self.id).count()
    
    def total_score(self):
        return sum(vote.score for vote in self.votes)

class VoteType:
    TIME_WORTH_IT = "Your time is worth it"
    MATH_CHECKS_OUT = "The math checks out"
    NOT_WORTH_IT = "This isn't worth it"
    MATH_DOESNT_CHECK = "The math doesn't check out"
    TREAT_YO_SELF = "Treat Yo Self"
    WHY_NOT = "Meh, why not"
    
    @classmethod
    def get_all_types(cls):
        return [cls.TIME_WORTH_IT, cls.MATH_CHECKS_OUT, cls.NOT_WORTH_IT, 
                cls.MATH_DOESNT_CHECK, cls.TREAT_YO_SELF, cls.WHY_NOT]

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    score = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<Vote {self.vote_type} on Post {self.post_id}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    votes = db.Column(db.Integer, default=0)
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    def __repr__(self):
        return f'<Comment {self.id}>'