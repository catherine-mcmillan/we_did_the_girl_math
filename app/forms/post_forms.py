from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.models.post import VoteType

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    expense = StringField('Expense or Purchase', validators=[DataRequired()])
    justification = TextAreaField('Justification', validators=[DataRequired()])
    is_seeking_help = BooleanField('I need help with the girl math')
    submit = SubmitField('Share')

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')

class VoteForm(FlaskForm):
    vote_type = SelectField('Vote', choices=[(vt, vt) for vt in VoteType.get_all_types()])
    submit = SubmitField('Vote')