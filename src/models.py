from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

follower_table = Table(
    "followers",
    db.Model.metadata,
    Column("follower_id", ForeignKey("user.id"), primary_key=True),
    Column("following_id", ForeignKey("user.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin=follower_table.c.follower_id == "user.id",
        secondaryjoin=follower_table.c.following_id == "user.id",
        back_populates="follower")
    follower: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin=follower_table.c.following_id == "user.id",
        secondaryjoin=follower_table.c.follower_id == "user.id",
        back_populates="following")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[User] = relationship(back_populates="posts")
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    media: Mapped[list["Media"]] = relationship(back_populates="posted_in")

    def serialize(self):
        return {
            "id": self.id,
            "comments": self.comments,
            "media": self.media
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(300))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    author: Mapped[User] = relationship(back_populates="comments")
    post: Mapped[Post] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))
    posted_in: Mapped[Post] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url
        }
