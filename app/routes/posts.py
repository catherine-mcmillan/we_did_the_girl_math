from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from app import db
from app.models.post import Post, Vote, Comment, VoteType
from app.forms.post_forms import PostForm, CommentForm, VoteForm

bp = Blueprint('posts', __name__)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            expense=form.expense.data,
            justification=form.justification.data,
            is_seeking_help=form.is_seeking_help.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        if post.is_seeking_help:
            return redirect(url_for('main.help_me_justify'))
        return redirect(url_for('main.index'))
    return render_template('posts/create.html', title='Create Post', form=form)

@bp.route('/<int:id>', methods=['GET', 'POST'])
def view(id):
    post = Post.query.get_or_404(id)
    vote_form = VoteForm()
    comment_form = CommentForm()
    
    # Handle comment submission
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You must be logged in to comment.')
            return redirect(url_for('auth.login', next=request.url))
        
        comment = Comment(
            body=comment_form.body.data,
            commenter=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!')
        return redirect(url_for('posts.view', id=post.id))
    
    comments = Comment.query.filter_by(post_id=post.id, parent_id=None).order_by(Comment.votes.desc()).all()
    
    return render_template('posts/view.html', title=post.title, post=post, 
                          vote_form=vote_form, comment_form=comment_form, comments=comments)

@bp.route('/<int:id>/vote', methods=['POST'])
@login_required
def vote(id):
    post = Post.query.get_or_404(id)
    form = VoteForm()
    
    if form.validate_on_submit():
        # Check if user already voted
        existing_vote = Vote.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        
        if existing_vote:
            existing_vote.vote_type = form.vote_type.data
        else:
            vote = Vote(
                vote_type=form.vote_type.data,
                voter=current_user,
                post=post
            )
            db.session.add(vote)
        
        db.session.commit()
        flash('Your vote has been recorded!')
    
    return redirect(url_for('posts.view', id=post.id))

@bp.route('/comment/<int:id>/upvote', methods=['POST'])
@login_required
def upvote_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.votes += 1
    db.session.commit()
    return redirect(url_for('posts.view', id=comment.post_id))

@bp.route('/comment/<int:id>/reply', methods=['POST'])
@login_required
def reply_to_comment(id):
    parent = Comment.query.get_or_404(id)
    form = CommentForm()
    
    if form.validate_on_submit():
        reply = Comment(
            body=form.body.data,
            commenter=current_user,
            post_id=parent.post_id,
            parent_id=parent.id
        )
        db.session.add(reply)
        db.session.commit()
        flash('Your reply has been posted!')
    
    return redirect(url_for('posts.view', id=parent.post_id))