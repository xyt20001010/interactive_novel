from flask import current_app
from models import db, Story, Chapter, Choice
from story_data import storyData

def init_db():
    """初始化数据库"""
    with current_app.app_context():
        db.create_all()

def add_sample_data():
    """添加示例数据"""            
    # 添加第二个故事
    add_story2()

def add_story2():
    """添加第二个故事数据"""
    with current_app.app_context():
        # 先清空story_id=2的所有相关数据
        Story.query.filter_by(id=2).delete()
        Chapter.query.filter_by(story_id=2).delete()
        Choice.query.filter_by(story_id=2).delete()
        
        # 创建第二个故事
        story2 = Story(id=2, title="错位的礼物", description="关于刘枭和Vein的互动故事")
        db.session.add(story2)
        db.session.commit()
        
        # 创建所有章节
        chapters = {}
        for scene_id, scene_data in storyData.items():
            chapter = Chapter(
                story_id=story2.id,
                title=scene_data["chapter"],
                content=scene_data["text"],
                is_start=(scene_id == "start"),
                audio=scene_data.get("audio", [])
            )
            db.session.add(chapter)
            chapters[scene_id] = chapter
        
        db.session.commit()
        
        # 创建所有选项
        for scene_id, scene_data in storyData.items():
            if "choices" in scene_data:
                for choice_data in scene_data["choices"]:
                    choice = Choice(
                        story_id=story2.id,
                        chapter_id=chapters[scene_id].id,
                        text=choice_data["text"],
                        next_chapter_id=chapters[choice_data["next"]].id
                    )
                    db.session.add(choice)
        
        db.session.commit()
        
        