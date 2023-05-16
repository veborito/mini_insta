from app  import db, login
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return f"User - {self.username}"
    
    def check_password(self, password_try):
        return self.password == password_try

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"Post - {self.text}"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))