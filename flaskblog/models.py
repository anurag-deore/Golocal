from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    skills = db.Column(db.Text, nullable=True, default='')
    location = db.Column(db.String(120), nullable=True)
    location_latlng = db.Column(db.String(120), nullable=True)
    # new additions
    address = db.Column(db.String(120), nullable=True)  # nerul,navi mumbai
    # [2,3,4,5,1,1,2,3,4] - take avg while displaying
    rating = db.Column(db.Integer, nullable=True)
    # [1,3,4,5,5] - list of user id's bookmarked
    bookmarks = db.Column(db.Text, nullable=True, default='')
    # [1,3,4,5,5]  - list of user id's chatted with
    chats = db.Column(db.Text, nullable=True, default='')
    # boolean 1 or 0 - if there are new chats
    notification = db.Column(db.Integer, nullable=True)

    # posts = db.relationship('Post', backref='author', lazy=True)
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "image_file": self.image_file,
            "category": self.category,
            "skills": [] if self.skills == None or self.skills == '' else self.skills.split(","),
            "location": self.location,
            "address": self.address,
            "rating": [] if self.rating == None or self.rating == '' else self.rating.split(","),
            "bookmarks": [] if self.bookmarks == None or self.bookmarks == '' else self.bookmarks.split(","),
            "chats": [] if self.chats == None or self.chats == '' else self.chats.split(","),
            "notification": self.notification,
        }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "time": self.date_posted.strftime("%b %d,%Y %H:%M"),
            "sender": self.sender,
            "receiver": self.receiver,
        }

    def __repr__(self):
        return f"Chat('{self.message}', '{self.sender}', '{self.receiver}')"

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     location = db.Column(db.String(100), nullable=False)
#     minsal = db.Column(db.Integer, nullable=False,default=0)
#     maxsal = db.Column(db.Integer, nullable=False,default=0)
#     applications = db.Column(db.Integer, nullable=False,default=0)
#     description = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"
