from core import models, schemas
from core import repositories
from core.services.base import BaseObjectService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class PostService(BaseObjectService):
    async def get_posts(self, db: AsyncSession, pagination: schemas.Pagination):

        all_posts = await self.repository.get_posts(db=db, limit=pagination.limit, skip=pagination.offset)
        return all_posts

    async def create_post(self, db: AsyncSession, user: models.User, data: schemas.CreatePost) -> schemas.Post:
        data_dict: dict = dict(data)
        data_dict['user_id'] = user.id
        post: models.Post = await self.repository.create(db=db, obj_in=data_dict)
        post.user = user
        return post

    async def get_post(self, db: AsyncSession, post_id: int) -> models.Post:
        post: models.Post = await self.repository.get_post_by_id(db=db, id=post_id)
        post.user = await repositories.user.get_by_id(db=db, id=post.user_id)
        return post

    async def delete_post(self, db: AsyncSession, post_id: int, current_user: models.User):
        post: models.Post = await self.repository.get_post_by_id(db=db, id=post_id, owner=current_user.id)
        await self.repository.delete_by_id(db=db, id=post.id)

    async def update_post(self, db: AsyncSession, post_id: int, data: schemas.UpdatePost, current_user: models.User):
        post: models.Post = await self.repository.get_post_by_id(db=db, id=post_id, owner=current_user.id)
        update_post: models.Post = await self.repository.update(db=db, db_obj=post, obj_in=data)
        return update_post


post_service = PostService(repository=repositories.post)
