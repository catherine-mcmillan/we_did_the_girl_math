from flask import Blueprint, render_template, request, current_app
from app.models.post import Post, VoteType
from flask_login import current_user
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_seeking_help=False).order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config.get('POSTS_PER_PAGE', 10), error_out=False)
    return render_template('index.html', 
                         title='Home', 
                         posts=posts.items, 
                         pagination=posts,
                         vote_types=VoteType.get_all_types())

@bp.route('/hall-of-fame')
def hall_of_fame():
    # Sort posts by total score in descending order
    posts = Post.query.filter_by(is_seeking_help=False).all()
    hall_of_fame_posts = sorted(posts, key=lambda p: p.total_score(), reverse=True)[:20]
    return render_template('hall_of_fame.html', 
                         title='Hall of Fame', 
                         posts=hall_of_fame_posts,
                         vote_types=VoteType.get_all_types())

@bp.route('/help-me-justify')
def help_me_justify():
    page = request.args.get('page', 1, type=int)
    help_posts = Post.query.filter_by(is_seeking_help=True).order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config.get('POSTS_PER_PAGE', 10), error_out=False)
    return render_template('help_justify.html', 
                         title='Help Me Justify', 
                         posts=help_posts.items, 
                         pagination=help_posts,
                         vote_types=VoteType.get_all_types())

@bp.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy', now=datetime.utcnow)