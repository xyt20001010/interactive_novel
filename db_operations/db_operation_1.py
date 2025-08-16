from flask import current_app
from models import db, Story, Chapter, Choice

def init_db():
    """初始化数据库"""
    with current_app.app_context():
        db.create_all()

def add_sample_data():
    """添加示例数据"""
    with current_app.app_context():
        if not Story.query.first():  # 如果数据库为空才添加示例数据
            # 创建故事
            story = Story(title="神秘岛冒险", description="一个关于神秘岛屿的冒险故事")
            db.session.add(story)
            db.session.commit()
            
            # 创建章节
            chapter1 = Chapter(story_id=story.id, title="登岛", 
                                content="你醒来发现自己在一个陌生的海滩上...", is_start=True)
            chapter2 = Chapter(story_id=story.id, title="丛林探险", 
                                content="你决定进入丛林探索...")
            chapter3 = Chapter(story_id=story.id, title="海滩等待", 
                                content="你决定留在海滩等待救援...")
            
            db.session.add_all([chapter1, chapter2, chapter3])
            db.session.commit()
            
            # 创建选择
            choice1 = Choice(story_id=story.id, chapter_id=chapter1.id, text="进入丛林探险", next_chapter_id=chapter2.id)
            choice2 = Choice(story_id=story.id, chapter_id=chapter1.id, text="留在海滩等待救援", next_chapter_id=chapter3.id)
            
            # 创建结局章节
            ending1 = Chapter(story_id=story.id, title="结局1", content="结局1...")
            ending2 = Chapter(story_id=story.id, title="结局2", content="结局2...")
            ending3 = Chapter(story_id=story.id, title="结局3", content="结局3...")
            ending4 = Chapter(story_id=story.id, title="结局4", content="结局4...")
            
            db.session.add_all([chapter1, chapter2, chapter3, ending1, ending2, ending3, ending4])
            db.session.commit()
            
            # 添加新的子选项
            choice1_sub1 = Choice(story_id=story.id, chapter_id=chapter2.id, text="去河边", next_chapter_id=ending1.id)
            choice1_sub2 = Choice(story_id=story.id, chapter_id=chapter2.id, text="去山谷", next_chapter_id=ending2.id)
            choice2_sub1 = Choice(story_id=story.id, chapter_id=chapter3.id, text="原地等待", next_chapter_id=ending3.id)
            choice2_sub2 = Choice(story_id=story.id,chapter_id=chapter3.id, text="沿海边走走", next_chapter_id=ending4.id)
            
            db.session.add_all([choice1, choice2, choice1_sub1, choice1_sub2, choice2_sub1, choice2_sub2])
            db.session.commit()
            


