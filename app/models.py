from app import db
from datetime import datetime


class Chat(db.Model):
    '''
    Table chat
    '''
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    msg = db.Column(db.VARCHAR(256))
    room = db.Column(db.VARCHAR(256))
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    # def __repr__(self):
    #     return '<Chat {0}>'.format(self.username)
    def __repr__(self):
        return f'username: {self.username}\nroom: {self.room}\nid: {self.id}'