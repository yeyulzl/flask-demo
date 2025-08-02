from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id       = db.Column(db.String(64), primary_key=True)  # openid
    nickname = db.Column(db.String(64))
    created  = db.Column(db.DateTime, default=datetime.utcnow)

class Inspiration(db.Model):
    __tablename__ = 'inspirations'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    title      = db.Column(db.String(100), nullable=False)
    content    = db.Column(db.Text, default='')
    priority   = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    archived   = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'archived': self.archived
        }