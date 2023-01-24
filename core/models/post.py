from .base import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'post'

    title = Column(String)
    content = Column(String)

    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[user_id], cascade="all, delete")


class LikeDislikePost(Base):
    __tablename__ = 'post_like_dislike'

    like = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])
    post_id = Column(Integer, ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    post = relationship("Post", foreign_keys=[post_id])


