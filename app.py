from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
# 初始化 Flask-Migrate
migrate = Migrate(app, db)  # 关键行：绑定 app 和 db

from db_operations import init_db, add_sample_data

# 初始化数据库
with app.app_context():
    init_db()
    add_sample_data()

@app.route('/')
def index():
    from models import Story
    stories = Story.query.all()
    return render_template('index.html', stories=stories)

@app.route('/story/<int:story_id>')
def story(story_id):
    from models import Chapter
    start_chapter = Chapter.query.filter_by(story_id=story_id, is_start=True).first()
    return redirect(url_for('chapter', story_id=story_id, chapter_id=start_chapter.id))

@app.route('/story/<int:story_id>/chapter/<int:chapter_id>')
def chapter(story_id, chapter_id):
    from models import Story, Chapter, Choice
    story = Story.query.get_or_404(story_id)
    chapter = Chapter.query.get_or_404(chapter_id)
    # 只查询没有父选项的顶级选项
    choices = Choice.query.filter_by(chapter_id=chapter_id, parent_choice_id=None).all()
    
    return render_template('chapter.html', 
                         story=story, 
                         chapter=chapter, 
                         choices=choices)

@app.template_filter('format_content')
def format_content(text):
    paragraphs = [f'<p>{p}</p>' for p in text.split('\n') if p]
    return ''.join(paragraphs)

if __name__ == '__main__':
    app.run(debug=True)