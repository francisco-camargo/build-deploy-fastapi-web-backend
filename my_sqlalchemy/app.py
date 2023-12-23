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
    post = Post(**post_create.dict())
    session.add(post)
    await session.commit()

    return post
