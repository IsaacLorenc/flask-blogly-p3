"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    ''''User on site'''
   
    __tablename__ ='user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False,)
    last_name = db.Column(db.Text, nullable=False)
    image_url =  db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationsship('Post', backref='user', cascade= 'all, delete-orphan')

@property
def full_name(self):
    '''Returns users full name'''

    return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    '''Blog post'''

    __tablename__='posts'

    id  = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.Text, nullable = False)
    content = db.Colummn(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeginKey('user.id'), nullable=False)

@property
def friendly_date(self):
    '''returns better formatted date'''

    return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

class PostTag(db.Model):
    '''Tags on post'''

    __tablename__='post_tags'

    post_id = db.Column(db.Integer, db.ForeginKey('Post.id'), primary_key=True)
    tag_id = db.Column(db.Integer,  db.ForeignKey('tag.id'), primary_key=True)

class Tag(db.Model):
    '''Tag that can be added to post'''

    __tablename__='tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)