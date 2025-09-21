from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Association table for likes
likes_table = Table(
    "likes",
    Base.metadata,
    Column("liker_id", Integer, ForeignKey("users.id")),
    Column("liked_id", Integer, ForeignKey("users.id")),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    interests = Column(String)
    avatar_url = Column(String)

    # relationships
    likes = relationship(
        "User",
        secondary=likes_table,
        primaryjoin=id == likes_table.c.liker_id,
        secondaryjoin=id == likes_table.c.liked_id,
        backref="liked_by"
    )
