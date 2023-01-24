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
        self, db: AsyncSession, *, id: int, owner: int = None, rise_not_exist: bool = True
    ) -> Optional[models.Post]:
        post = await self.get_by_id(db=db, id=id)

        if post is None and rise_not_exist:
            raise HTTPException(status_code=404, detail=f"Post not found")

        if owner is not None and owner != post.user_id:
            raise HTTPException(status_code=404, detail=f"You are`t author this post")

        return post


post = PostRepository(model=models.Post)
