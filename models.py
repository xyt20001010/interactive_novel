from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    chapters = db.relationship('Chapter', backref='story', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    is_start = db.Column(db.Boolean, default=False)
    choices = db.relationship('Choice', 
                            backref='chapter', 
                            lazy=True,
                            foreign_keys='Choice.chapter_id')  # 指定外键

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    next_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    # parent_choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))
    # sub_choices = db.relationship('Choice', backref=db.backref('parent_choice', remote_side='Choice.id'))