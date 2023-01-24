from core import services, schemas, models
from core.api import depends

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


router = APIRouter()


@router.get('/posts', status_code=200, response_model=List[schemas.Post])
async def get_posts(
    pagination: schemas.Pagination = Depends(schemas.Pagination),
    db: AsyncSession = Depends(depends.get_session),
):
    """Endpoint to get posts list"""
    posts: List[models.Post] = await services.post_service.get_posts(db=db, pagination=pagination)
    return posts


@router.post('/post/add', status_code=201, response_model=schemas.Post)
async def create_post(
    data: schemas.CreatePost,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
):
    """Endpoint to create post"""
    created_post: models.Post = await services.post_service.create_post(db=db, data=data, user=current_user)
    return created_post


@router.get('/post/{post_id}', status_code=200, response_model=schemas.Post)
async def view_post(
    post_id: int,
    db: AsyncSession = Depends(depends.get_session),
):
    """Endpoint to view post"""
    post: models.Post = await services.post_service.get_post(db=db, post_id=post_id)

    return post


@router.patch('/post/{post_id}', status_code=200, response_model=schemas.Post)
async def update_post(
    post_id: int,
    data: schemas.UpdatePost,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
):
    """Endpoint to edit post"""
    post = await services.post_service.update_post(db=db, post_id=post_id, data=data, current_user=current_user)
    return post


@router.delete('/post/{post_id}', status_code=200, )
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
):
    """Endpoint to delete post"""
    await services.post_service.delete_post(db=db, post_id=post_id, current_user=current_user)
    return {"message": "Successfully deleted"}


@router.patch('/post/{post_id}/like', status_code=204, )
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
) -> None:
    """Endpoint to delete post"""


@router.patch('/post/{post_id}/dislike', status_code=204, )
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_user),
) -> None:
    """Endpoint to delete post"""


