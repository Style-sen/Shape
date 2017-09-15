#-*-coding:utf-8-*-
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from main.ext import bcrypt

"""
建立数据模型
"""
class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        "Post",
        backref = "user",
        lazy = "dynamic"
    )

    def __init__(self,username):
        self.username = username
    def __repr__(self):
        return "<User %s>".format(self.username)
    def set_password(self,password):
        self.password = bcrypt.generate_password_hash(password)
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)

tags =  db.Table("post_tag",
                 db.Column("post_id",db.Integer,db.ForeignKey("post.id")),
                 db.Column("tag_id",db.Integer,db.ForeignKey("tag.id"))
                 )



class Post(db.Model):
    __tablename__="post"
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(255),index=True)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    comments = db.relationship(
        "Comment",
        backref="post",
        lazy="dynamic"
    )
    user_id = db.Column(db.Integer(),db.ForeignKey("user.id"))
    tags = db.relationship("Tag",
                           secondary=tags,
                           backref=db.backref("posts",lazy="dynamic")
                           )

    def __init__(self,title):
        self.title = title

    def __repr__(self):
        return "<Post %s>".format(self.title)

class Comment(db.Model):
    __tablename__="comment"
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(),db.ForeignKey("post.id"))

    def __repr__(self):
        return "<Comment %s>".format(self.text[:15])

class Tag(db.Model):
    __tablename__="tag"
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(255),index=True)

    def __init__(self,title):
        self.title=title

    def __repr__(self):
        return "<Tag %s>".format(self.title)