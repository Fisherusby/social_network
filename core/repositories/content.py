from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from core import models, schemas
from core.repositories.base import BaseRepository


class ContentRepository(BaseRepository[models.Post, schemas.CreatePost, schemas.UpdatePost]):
    async def get_posts(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        user: Optional[models.User] = None,
    ) -> List[models.Post]:
        """Get all posts with current user like status."""
        if user is not None:
            sub_query = (
                select(models.LikeDislikePost.post_id, models.LikeDislikePost.like)
                .filter(models.LikeDislikePost.user_id == user.id)
                .subquery()
            )

            query = (
                select(self.model, sub_query.c.like.label("like"))
                .join(sub_query, and_(sub_query.c.post_id == self.model.id), isouter=True)
                .options(selectinload(self.model.user))
                .order_by(models.Post.created_at.desc())
            )
            result: List[models.Post] = []
            posts = (await db.execute(query.offset(skip).limit(limit))).all()
            for post, like in posts:
                post.like = like
                result.append(post)
            return result
        else:
            query = select(self.model).options(selectinload(self.model.user)).order_by(models.Post.created_at.desc())
            return (await db.execute(query.offset(skip).limit(limit))).scalars().all()

    async def get_user_like_post(self, db: AsyncSession, post_id: UUID, user_id: UUID) -> models.LikeDislikePost:
        """Get posts likes status for user."""
        query = (
            select(models.LikeDislikePost)
            .filter(models.LikeDislikePost.user_id == user_id)
            .filter(models.LikeDislikePost.post_id == post_id)
        )
        return (await db.execute(query)).scalar_one_or_none()

    async def set_like(self, db: AsyncSession, post_id: UUID, user_id: UUID, like: bool):
        """Set post likes status for user."""
        odj_data: dict = {'user_id': user_id, 'post_id': post_id, 'like': like}
        db_obj: models.LikeDislikePost = models.LikeDislikePost(**odj_data)
        db.add(db_obj)
        await db.flush()
        await db.commit()

    async def unset_like(self, db: AsyncSession, like_obj: models.LikeDislikePost):
        """Unset post likes status for user."""
        await db.delete(like_obj)
        await db.commit()

    async def calculate_like(self, db: AsyncSession, post_id: UUID, like: bool) -> int:
        """Calculate count of likes and dislikes for post."""
        sub_query = (
            select(models.LikeDislikePost)
            .filter(models.LikeDislikePost.post_id == post_id)
            .filter(models.LikeDislikePost.like == like)
        )
        query = select(func.count()).select_from(sub_query.subquery())
        return (await db.execute(query)).scalar()


content = ContentRepository(model=models.Post)
