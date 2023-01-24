from core import models, schemas
from core import repositories
from core.services.base import BaseObjectService
from core.config import contstants
from sqlalchemy.ext.asyncio import AsyncSession


class PostService(BaseObjectService):
    async def get_posts(self, db: AsyncSession, pagination: schemas.Pagination):
        """Get all posts."""
        all_posts = await self.repository.get_posts(db=db, limit=pagination.limit, skip=pagination.offset)
        return all_posts

    async def create_post(self, db: AsyncSession, user: models.User, data: schemas.CreatePost) -> schemas.Post:
        """Create post."""
        data_dict: dict = dict(data)
        data_dict['user_id'] = user.id
        post: models.Post = await self.repository.create(db=db, obj_in=data_dict)
        post.user = user
        return post

    async def get_post(self, db: AsyncSession, post_id: int) -> models.Post:
        """Get a post."""
        post: models.Post = await self.repository.get_post_by_id(db=db, id=post_id)
        post.user = await repositories.user.get_by_id(db=db, id=post.user_id)
        return post

    async def delete_post(self, db: AsyncSession, post_id: int, current_user: models.User):
        """Delete your post by id"""
        post: models.Post = await self.repository.get_post_by_id(db=db, id=post_id, user_id=current_user.id, owner=True)
        await self.repository.delete_by_id(db=db, id=post.id)

    async def update_post(self, db: AsyncSession, post_id: int, data: schemas.UpdatePost, current_user: models.User):
        """Update your post by id"""
        post: models.Post = await self.repository.get_post_by_id(db=db, id=post_id, user_id=current_user.id, owner=True)
        update_post: models.Post = await self.repository.update(db=db, db_obj=post, obj_in=data)
        return update_post

    async def like_post(self, db: AsyncSession, post_id: int, current_user: models.User, like: bool):
        await self.repository.get_post_by_id(
            db=db, post_id=post_id, user_id=current_user.id, owner=False
        )
        user_like_post: models.LikeDislikePost = await self.repository.get_user_like_post(
            db=db, post_id=post_id, user_id=current_user.id
        )

        if user_like_post is None:
            await self.repository.set_like(db=db, post_id=post_id, user_id=current_user.id, like=like)
            return {'message': f"Successful set {contstants.like_types[like]}"}
        elif user_like_post.like == like:
            await self.repository.unset_like(db=db, like_obj=user_like_post)
            return {'message': f"Successful unset {contstants.like_types[like]}"}
        else:
            await self.repository.unset_like(db=db, like_obj=user_like_post)
            await self.repository.set_like(db=db, post_id=post_id, user_id=current_user.id, like=like)
            return {'message': f"Successful set {contstants.like_types[like]}"}


post_service = PostService(repository=repositories.post)
