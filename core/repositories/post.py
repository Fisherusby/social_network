from core.repositories.base import BaseRepository
from core import models
from typing import List, Optional
from sqlalchemy import func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException


class PostRepository(BaseRepository):
    async def get_posts(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        user: models.User = None,
    ) -> List[models.Post]:
        """Get all posts with current user like status."""
        if user is not None:
            sub_query = select(models.LikeDislikePost.post_id, models.LikeDislikePost.like)\
                .filter(models.LikeDislikePost.user_id == user.id).subquery()

            query = select(self.model, sub_query.c.like.label("like")).join(
                sub_query, and_(
                    sub_query.c.post_id == self.model.id), isouter=True
            )
            query = query.options(selectinload(self.model.user))
            result = []
            for row in (await db.execute(query.offset(skip).limit(limit))).all():
                post, like = row
                post.like = like
                result.append(post)
            return result
        else:
            query = select(self.model)
            query = query.options(selectinload(self.model.user))
            return (await db.execute(query.offset(skip).limit(limit))).scalars().all()

    async def get_post_by_id(
        self,
        db: AsyncSession,
        *,
        post_id: int,
        user_id: int = None,
        owner: bool = None,
        rise_not_exist: bool = True,
    ) -> Optional[models.Post]:
        """Get post with current user like status.

        Check user for this post's owner"""
        post = await self.get_by_id(db=db, id=post_id)

        if user_id is not None:
            post_like: models.LikeDislikePost = await self.get_user_like_post(db=db, post_id=post_id, user_id=user_id)
            if post_like is not None:
                post.like = post_like.like
        if post is None and rise_not_exist:
            raise HTTPException(status_code=404, detail=f"Post not found")

        if owner is not None and user_id is not None:
            if owner and user_id != post.user_id:
                raise HTTPException(status_code=404, detail=f"You are`t author this post")

            if not owner and user_id == post.user_id:
                raise HTTPException(status_code=404, detail=f"You are author this post")

        return post

    async def get_user_like_post(self, db: AsyncSession, post_id: int, user_id: int):
        """Get posts likes status for user"""
        query = select(models.LikeDislikePost)\
            .filter(models.LikeDislikePost.user_id == user_id)\
            .filter(models.LikeDislikePost.post_id == post_id)
        return (await db.execute(query)).scalar_one_or_none()

    async def set_like(self, db: AsyncSession, post_id: int, user_id: int, like: bool):
        """Set post likes status for user"""
        odj_data: dict = {
            'user_id': user_id,
            'post_id': post_id,
            'like': like
        }
        db_obj: models.LikeDislikePost = models.LikeDislikePost(**odj_data)
        db.add(db_obj)
        await db.flush()
        await db.commit()

    async def unset_like(self, db: AsyncSession, like_obj: models.LikeDislikePost):
        """Unset post likes status for user"""
        await db.delete(like_obj)
        await db.commit()

    async def calculate_like(self, db: AsyncSession, post_id: int, like:bool) -> int:
        """Calculate count of likes and dislikes for post"""
        sub_query = select(models.LikeDislikePost)\
            .filter(models.LikeDislikePost.post_id == post_id)\
            .filter(models.LikeDislikePost.like == like)
        query = select(func.count()).select_from(sub_query.subquery())
        return (await db.execute(query)).scalar()


post = PostRepository(model=models.Post)
