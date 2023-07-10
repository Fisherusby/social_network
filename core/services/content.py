from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core import models, repositories, schemas, services
from core.config import contstants
from core.services.base import BaseObjectService


class ContentService(BaseObjectService):
    async def get_posts(
        self, db: AsyncSession, pagination: schemas.Pagination, user: Optional[models.User] = None
    ) -> List[schemas.PostWithInfo]:
        """Get all posts."""
        posts: List[models.Post] = await self.repository.get_posts(
            db=db, user=user, limit=pagination.limit, skip=pagination.offset
        )
        return [
            schemas.PostWithInfo(**post.dict(), like_count=await self._get_cache_post_like(db=db, post_id=post.id))
            for post in posts
        ]

    async def create_post(self, db: AsyncSession, user: models.User, data: schemas.CreatePost) -> schemas.Post:
        """Create post."""
        data_dict: dict = dict(data)
        data_dict['user_id'] = user.id
        post: models.Post = await self.repository.create(db=db, obj_in=data_dict)
        return schemas.Post(**post.dict(), user=user)

    async def get_post(
        self, db: AsyncSession, post_id: UUID, user: Optional[models.User] = None
    ) -> schemas.PostWithInfo:
        """Get a post."""
        user_id = user.id if user is not None else None
        post: models.Post = await self.get_and_check_post_by_id(db=db, post_id=post_id, user_id=user_id)
        return schemas.PostWithInfo(
            **post.dict(),
            user=await repositories.user.get_by_id(db=db, id=post.user_id),
            like_count=await self._get_cache_post_like(db=db, post_id=post.id),
        )

    async def get_and_check_post_by_id(
        self,
        db: AsyncSession,
        *,
        post_id: UUID,
        user_id: UUID = None,
        owner: bool = None,
        rise_not_exist: bool = True,
    ) -> Optional[models.Post]:
        """Get post with current user like status.

        Check user for this post's owner
        """
        post = await self.repository.get_by_id(db=db, id=post_id)

        if post is None and rise_not_exist:
            raise HTTPException(status_code=404, detail=f"Post not found")

        if owner is not None and user_id is not None:
            if owner is True and user_id != post.user_id:
                raise HTTPException(status_code=404, detail=f"You are`t author this post")

            if owner is False and user_id == post.user_id:
                raise HTTPException(status_code=404, detail=f"You are author this post")

        if user_id is not None:
            post_like: models.LikeDislikePost = await self.repository.get_user_like_post(
                db=db, post_id=post_id, user_id=user_id
            )
            if post_like is not None:
                post.like = post_like.like

        return post

    async def delete_post(self, db: AsyncSession, post_id: UUID, current_user: models.User) -> None:
        """Delete your post by id."""
        post: models.Post = await self.get_and_check_post_by_id(
            db=db, post_id=post_id, user_id=current_user.id, owner=True
        )
        await self.repository.delete_by_id(db=db, id=post.id)

    async def update_post(
        self, db: AsyncSession, post_id: UUID, data: schemas.UpdatePost, current_user: models.User
    ) -> schemas.PostWithInfo:
        """Update your post by id."""
        post: models.Post = await self.get_and_check_post_by_id(
            db=db, post_id=post_id, user_id=current_user.id, owner=True
        )
        update_post: models.Post = await self.repository.update(db=db, db_obj=post, obj_in=data)
        return schemas.PostWithInfo(
            **update_post.dict(), user=current_user, like_count=await self._get_cache_post_like(db=db, post_id=post.id)
        )

    async def like_post(self, db: AsyncSession, post_id: UUID, current_user: models.User, like: bool) -> dict:
        await self.get_and_check_post_by_id(db=db, post_id=post_id, user_id=current_user.id, owner=False)
        user_like_post: models.LikeDislikePost = await self.repository.get_user_like_post(
            db=db, post_id=post_id, user_id=current_user.id
        )

        await self._get_cache_post_like(db=db, post_id=post_id)

        if user_like_post is None:
            await self.repository.set_like(db=db, post_id=post_id, user_id=current_user.id, like=like)
            await self._inc_cache_post_like(post_id=post_id, like=like)
            return {'message': f"Successful set {contstants.like_types[like]}"}

        if user_like_post.like == like:
            await self.repository.unset_like(db=db, like_obj=user_like_post)
            await self._inc_cache_post_like(post_id=post_id, like=like, inc=-1)
            return {'message': f"Successful unset {contstants.like_types[like]}"}

        await self.repository.unset_like(db=db, like_obj=user_like_post)
        await self._inc_cache_post_like(post_id=post_id, like=not like, inc=-1)
        await self.repository.set_like(db=db, post_id=post_id, user_id=current_user.id, like=like)
        await self._inc_cache_post_like(post_id=post_id, like=like)
        return {'message': f"Successful set {contstants.like_types[like]}"}

    async def _inc_cache_post_like(self, post_id: UUID, like: bool, inc: int = 1) -> None:
        key_data = f'{post_id}_{contstants.like_types[like]}'
        await services.redis_service.incrby(key_data, amount=inc)

    async def _get_cache_post_like(self, db: AsyncSession, post_id: UUID, recalc: bool = False) -> schemas.LikeDislike:
        """"""
        key_prefix = f'{post_id}_'
        like_data = {}

        for like_type_key, like_type_value in contstants.like_types.items():
            key_data = key_prefix + like_type_value
            like_value_in_memory = await services.redis_service.get(key_data)
            if like_value_in_memory is None or recalc:
                like_value_in_memory = await self.repository.calculate_like(db=db, post_id=post_id, like=like_type_key)
                await services.redis_service.set(key_data, like_value_in_memory)
            like_data[like_type_value] = like_value_in_memory

        likes_data: schemas.LikeDislike = schemas.LikeDislike(**like_data)
        return likes_data


content_service = ContentService(repository=repositories.content)
