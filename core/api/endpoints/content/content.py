from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import models, schemas, services
from core.api import depends
from core.config import contstants

router = APIRouter()


@router.get('/posts', status_code=200, response_model=List[schemas.PostWithInfo])
async def get_posts(
    pagination: schemas.Pagination = Depends(schemas.Pagination),
    current_user: Optional[models.User] = Depends(depends.get_current_user_or_none),
    db: AsyncSession = Depends(depends.get_session),
) -> List[schemas.PostWithInfo]:
    """Endpoint to get posts list."""
    posts: List[schemas.PostWithInfo] = await services.content_service.get_posts(
        db=db, pagination=pagination, user=current_user
    )
    return posts


@router.post('/post/add', status_code=201, response_model=schemas.Post)
async def create_post(
    data: schemas.CreatePost,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
) -> schemas.Post:
    """Endpoint to create a post."""
    created_post: schemas.Post = await services.content_service.create_post(db=db, data=data, user=current_user)
    return created_post


@router.get('/post/{post_id}', status_code=200, response_model=schemas.PostWithInfo)
async def view_post(
    post_id: UUID,
    current_user: Optional[models.User] = Depends(depends.get_current_user_or_none),
    db: AsyncSession = Depends(depends.get_session),
) -> schemas.PostWithInfo:
    """Endpoint to view a post."""
    post: schemas.PostWithInfo = await services.content_service.get_post(db=db, post_id=post_id, user=current_user)

    return post


@router.patch('/post/{post_id}', status_code=200, response_model=schemas.Post)
async def update_post(
    post_id: UUID,
    data: schemas.UpdatePost,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
) -> schemas.Post:
    """Endpoint to edit a post."""
    post: schemas.Post = await services.content_service.update_post(
        db=db, post_id=post_id, data=data, current_user=current_user
    )
    return post


@router.delete('/post/{post_id}', status_code=200)
async def delete_post(
    post_id: UUID,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
) -> dict:
    """Endpoint to delete a post."""
    await services.content_service.delete_post(db=db, post_id=post_id, current_user=current_user)
    return {"message": "Successfully deleted"}


@router.patch('/post/{post_id}/like', status_code=200)
async def like_post(
    post_id: UUID,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
) -> dict:
    """Endpoint to like a post."""

    return await services.content_service.like_post(
        db=db, post_id=post_id, current_user=current_user, like=contstants.post_like
    )


@router.patch('/post/{post_id}/dislike', status_code=200)
async def dislike_post(
    post_id: UUID,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
) -> dict:
    """Endpoint to dislike a post."""

    return await services.content_service.like_post(
        db=db, post_id=post_id, current_user=current_user, like=contstants.post_dislike
    )
