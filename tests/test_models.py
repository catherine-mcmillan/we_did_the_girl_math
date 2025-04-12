from app.models.user import User
from app.models.post import Post, Vote, Comment, VoteType

def test_user_password_hashing(app):
    with app.app_context():
        user = User(username='kat', email='kat-is-awesome@example.com')
        user.set_password('cat')
        assert not user.check_password('dog')
        assert user.check_password('cat')

def test_post_creation(app, test_user):
    with app.app_context():
        post = Post(title='Test Post', expense='$100 shoes', 
                    justification='They were on sale', author=test_user)
        assert post.author.username == 'testuser'
        assert post.expense == '$100 shoes'
        assert post.is_seeking_help is False

def test_voting(app, test_user):
    with app.app_context():
        post = Post(title='Test Post', expense='$100 shoes', 
                    justification='They were on sale', author=test_user)
        vote = Vote(vote_type=VoteType.MATH_CHECKS_OUT, voter=test_user, post=post)
        assert vote.vote_type == "The math checks out"
        assert vote.voter.username == 'testuser'