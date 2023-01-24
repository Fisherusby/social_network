from .base import Base
from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Table
from sqlalchemy.orm import relationship, backref


# mtm_in_favorite = Table(
#     'favorite_blog',
#     Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
#     Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
# )
#
# mtm_likes = Table(
#     'post_likes',
#     Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
#     Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
# )
#
# mtm_dislikes = Table(
#     'blog_dislikes',
#     Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
#     Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
# )
#
# mtm_tags = Table(
#     'blog_tags',
#     Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
#     Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
# )


class Post(Base):
    __tablename__ = 'post'

    title = Column(String)
    content = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # user = relationship("User", foreign_keys=[user_id], backref=backref('favorite_blogs'))
    user = relationship("User", foreign_keys=[user_id])


