from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5442/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
