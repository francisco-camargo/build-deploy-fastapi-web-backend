import contextlib
from collections.abc import Sequence

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from my_sqlalchemy import schemas
from my_sqlalchemy.database import (
    create_all_tables,
    get_async_session,
)
from my_sqlalchemy.models import Post


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Makes sure our schema is created when our application
    starts.
    '''
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


@app.get(
    '/posts',
    response_model=list[schemas.PostRead],
)
async def list_posts(
    pagination: tuple[int, int] = Depends(pagination),
    session: AsyncSession = Depends(get_async_session),
) -> Sequence[Post]:
    '''
    Obtain all posts, given skip and limit parameters
    '''
    skip, limit = pagination
    select_query = select(Post).offset(skip).limit(limit)
    result = await session.execute(select_query)

    return result.scalars().all()


@app.post(
    '/posts',
    response_model=schemas.PostRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post_create: schemas.PostPartialUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    '''
    Add a post to the db by providing title and content
    '''
    post = Post(**post_create.dict())
    session.add(post)
    await session.commit()

    return post


async def get_post_or_404(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    '''
    Find post given id, return exception if id not found
    '''
    select_query = select(Post).where(Post.id == id)
    result = await session.execute(select_query)
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post


@app.get(
    '/posts/{id}',
    response_model=schemas.PostRead,
)
async def get_post(post: Post = Depends(get_post_or_404)) -> Post:
    '''
    Route to return post based on id given
    '''
    return post
