import asyncio
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import create_async_engine

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(128), index=True)
    password = Column(String(128), index=True)

    role = Column(Integer, ForeignKey(
        'roles.id',
        ondelete='CASCADE'
        )
    )

    roles = relationship('Roles', back_populates='users', lazy='subquery')


    def __repr__(self):
        return f'{self.id} - {self.login} - {self.password} - {self.role}'


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), index=True)
    level = Column(Integer, index=True, unique=True)

    users = relationship('User', back_populates='roles', lazy='subquery')

    def __repr__(self):
        return f'{self.id} - {self.name} - {self.level}'



async def create_db():
    PG_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5642/postgres'

    engine = create_async_engine(PG_URL)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)



if __name__ == '__main__':
    asyncio.run(create_db())