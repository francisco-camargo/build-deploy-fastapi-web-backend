'''
Set up the connection between the FastAPI app and the
database engine.
'''

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from my_sqlalchemy.models import Base

DATABASE_URL = 'sqlite+aiosqlite:///chapter06_sqlalchemy.db'
    # This string specifies the following
        # the database engine; sqlite
        # Optional driver; aiosqlite
        # Optional authentication information
        # Hostname of the database server. For SQLite we
            # just need to specify the path of the file that
            # will store all the data
    # For more info
        # https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
    # Could alternatively create URLs programmatically
        # https://docs.sqlalchemy.org/en/20/core/engines.html#creating-urls-programmatically
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine=engine,
    expire_on_commit=False,
    )

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        
        
async def create_all_tables():
    '''
    Create the table's schema inside the database. This is a
    simple example, in real-world projects we would need a 
    proper migration system.
    
    To make sure the schema is created when the application
    starts, we must call this function as part of the 
    lifespan handler of FastAPI defined in app.py
    '''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
