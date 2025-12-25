from datetime import datetime

class ToolkitItem:
    def __init__(self, title, type, category, content_url, description="", thumbnail=""):
        self.title = title
        self.type = type  # 'video', 'activity', or 'story'
        self.category = category 
        self.content_url = content_url
        self.description = description
        self.thumbnail = thumbnail
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "title": self.title,
            "type": self.type,
            "category": self.category,
            "content_url": self.content_url,
            "description": self.description,
            "thumbnail": self.thumbnail,
            "created_at": self.created_at
        }