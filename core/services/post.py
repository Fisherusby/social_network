from uuid import UUID

from core import models, schemas, services
from core import repositories
from core.services.base import BaseObjectService
from core.config import contstants
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional


class PostService(BaseObjectService):
    async def get_posts(
            self, db: AsyncSession, pagination: schemas.Pagination, user: Optional[models.User] = None
    ) -> List[models.Post]:
        """Get all posts."""
        all_posts: List[models.Post] = await self.repository.get_posts(
            db=db, user=user, limit=pagination.limit, skip=pagination.offset
        )
        return [await self._attach_post_info(db=db, post=post) for post in all_posts]

    async def create_post(self, db: AsyncSession, user: models.User, data: schemas.CreatePost) -> schemas.Post:
        """Create post."""
        data_dict: dict = dict(data)
        data_dict['user_id'] = user.id
        post: models.Post = await self.repository.create(db=db, obj_in=data_dict)
        post.user = user
        return post

    async def get_post(self, db: AsyncSession, post_id: UUID, user: Optional[models.User] = None) -> models.Post:
        """Get a post."""
        user_id = user.id if user is not None else None
        post: models.Post = await self.repository.get_post_by_id(db=db, post_id=post_id, user_id=user_id)
        post.user = await repositories.user.get_by_id(db=db, id=post.user_id)
        return await self._attach_post_info(db=db, post=post)

    async def _attach_post_info(self, db: AsyncSession, post: models.Post) -> models.Post:
        post.like_count = await self._get_cache_post_like(db=db, post_id=post.id)
        return post

    async def delete_post(self, db: AsyncSession, post_id: UUID, current_user: models.User) -> None:
        """Delete your post by id"""
        post: models.Post = await self.repository.get_post_by_id(
            db=db, post_id=post_id, user_id=current_user.id, owner=True
        )
        await self.repository.delete_by_id(db=db, id=post.id)

    async def update_post(
            self, db: AsyncSession, post_id: UUID, data: schemas.UpdatePost, current_user: models.User
    ) -> models.Post:
        """Update your post by id"""
        post: models.Post = await self.repository.get_post_by_id(
            db=db, post_id=post_id, user_id=current_user.id, owner=True
        )
        update_post: models.Post = await self.repository.update(db=db, db_obj=post, obj_in=data)
        return await self._attach_post_info(db=db, post=update_post)

    async def like_post(self, db: AsyncSession, post_id: UUID, current_user: models.User, like: bool) -> dict:
        await self.repository.get_post_by_id(
            db=db, post_id=post_id, user_id=current_user.id, owner=False
        )
        user_like_post: models.LikeDislikePost = await self.repository.get_user_like_post(
            db=db, post_id=post_id, user_id=current_user.id
        )

        await self._get_cache_post_like(db=db, post_id=post_id)

        if user_like_post is None:
            await self.repository.set_like(db=db, post_id=post_id, user_id=current_user.id, like=like)
            await self._inc_cache_post_like(post_id=post_id, like=like)
            return {'message': f"Successful set {contstants.like_types[like]}"}
        elif user_like_post.like == like:
            await self.repository.unset_like(db=db, like_obj=user_like_post)
            await self._inc_cache_post_like(post_id=post_id, like=like, inc=-1)
            return {'message': f"Successful unset {contstants.like_types[like]}"}
        else:
            await self.repository.unset_like(db=db, like_obj=user_like_post)
            await self._inc_cache_post_like(post_id=post_id, like=not like, inc=-1)
            await self.repository.set_like(db=db, post_id=post_id, user_id=current_user.id, like=like)
            await self._inc_cache_post_like(post_id=post_id, like=like)
            return {'message': f"Successful set {contstants.like_types[like]}"}

    async def _inc_cache_post_like(self, post_id: UUID, like: bool, inc: int = 1) -> None:
        key_data = f'{post_id}_{contstants.like_types[like]}'
        await services.redis_service.incrby(key_data, amount=inc)

    async def _get_cache_post_like(self, db: AsyncSession, post_id: UUID, recalc: bool = False) -> schemas.LikeDislike:
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


post_service = PostService(repository=repositories.post)
