import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, String, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(200))

class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(50), index=True)
    first_name = Column(String(50), index=True)
    faculty = Column(String(50), index=True)
    course = Column(String(50), index=True)
    mark = Column(Integer, index=True)

    def __repr__(self):
        return f'{self.id} - {self.last_name} - {self.first_name} - {self.faculty} - {self.course} - {self.mark}'


async def create_db():
    PG_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5442/postgres'

    engine = create_async_engine(PG_URL)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)





if __name__ == '__main__':
    asyncio.run(create_db())

