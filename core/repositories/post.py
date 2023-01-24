from core.repositories.base import BaseRepository
from core import models
from typing import List, Optional
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

    ) -> List[models.Post]:
        # query = select(self.model)
        query = select(self.model).options(selectinload(self.model.user))
        return (await db.execute(query.offset(skip).limit(limit))).scalars().all()

    async def get_post_by_id(
        self, db: AsyncSession, *, post_id: int, user_id: int = None, owner: bool = None, rise_not_exist: bool = True
    ) -> Optional[models.Post]:
        post = await self.get_by_id(db=db, id=post_id)

        if post is None and rise_not_exist:
            raise HTTPException(status_code=404, detail=f"Post not found")

        if owner is not None and user_id is not None:
            if owner and user_id != post.user_id:
                raise HTTPException(status_code=404, detail=f"You are`t author this post")

            if not owner and user_id == post.user_id:
                raise HTTPException(status_code=404, detail=f"You are author this post")

        return post

    async def get_user_like_post(self, db: AsyncSession, post_id: int, user_id: int):
        query = select(models.LikeDislikePost)\
            .filter(models.LikeDislikePost.user_id == user_id)\
            .filter(models.LikeDislikePost.post_id == post_id)
        return (await db.execute(query)).scalar_one_or_none()

    async def set_like(self, db: AsyncSession, post_id: int, user_id: int, like: bool):
        db_obj: models.LikeDislikePost = models.LikeDislikePost(user_id=user_id, post_id=post_id, like=like)
        db.add(db_obj)
        await db.flush()
        await db.commit()

    async def unset_like(self, db: AsyncSession, like_obj: models.LikeDislikePost):
        await db.delete(like_obj)
        await db.commit()


post = PostRepository(model=models.Post)
