from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

follower_table = Table(
    "followers",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("follower_id", ForeignKey("follower.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    comments: Mapped[list["Comment"]] = relationship()
    posts: Mapped[list["Post"]] = relationship()
    followers: Mapped[list["Follower"]] = relationship(
        "Follower",
        secondary=follower_table,
        back_populates="followed_by"
    )


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    followed_by: Mapped[list[User]] = relationship(
        "User",
        secondary=follower_table,
        back_populates="followers"
    )
    
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[User] = relationship(back_populates="posts")
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    comments: Mapped[list["Comment"]] = relationship()
    media: Mapped[list["Media"]] = relationship()

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
    
    # author: Mapped[User] = relationship(back_populates="comments")


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
        return{
            "id": self.id,
            "url": self.url
        }
    


