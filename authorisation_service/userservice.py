from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from sqlalchemy import select, delete
from models import User, Roles

async def add_role(name, level):
    PG_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5642/postgres'

    engine = create_async_engine(PG_URL)

    session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    role = Roles(name=name, level=level)

    async with session() as db:
        db.add(role)
        await db.commit()

        return role


class RoleService():
    def __init__(self, db_url):
        self.db_url = db_url

    def get_async_session(self) -> AsyncSession:
        engine = create_async_engine(self.db_url)

        return sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
    )

    async def add_role(self, name, level):

        session = self.get_async_session()

        role = Roles(name=name, level=level)

        async with session() as db:
            db.add(role)
            await db.commit()

            return role

    async def get_roles(self):

        session = self.get_async_session()


        async with session() as db:
            roles = await db.execute(select(Roles))
            return roles.scalars().all()

    async def get_role(self, id):

        session = self.get_async_session()


        async with session() as db:
            role = await db.execute(select(Roles).where(Roles.id==id))
            return role.one()


class UserService():
    def __init__(self, db_url):
        self.db_url = db_url

    def get_async_session(self) -> AsyncSession:
        engine = create_async_engine(self.db_url)

        return sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
    )

    async def get_user(self, id):

        session = self.get_async_session()

        async with session() as db:
            user = await db.execute(select(User).where(User.id==id))
            return user.one()

    async def add_user(self, login, password, role):

        session = self.get_async_session()

        user = User(login=login, password=password, role=role)

        async with session() as db:
            db.add(user)
            await db.commit()

            return user

    async def update_user(self, id, **kwargs):

        session = self.get_async_session()

        async with session() as db:
            user = await db.execute(select(User).where(User.id==id))

            user = user.scalars().one()

            for key, value in kwargs.items():
                setattr(user, key, value)

            await db.commit()
            return user

    async def del_user(self, id):
        session = self.get_async_session()

        async with session() as db:
            user = await db.execute(delete(User).where(User.id == id))

            await db.commit()
            return user


async def runner():
    PG_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5642/postgres'
    role_service = RoleService(PG_URL)
    user_service = UserService(PG_URL)


#   res = await role_service.add_role(name='user', level=1)
#   res = await role_service.get_roles()
#   res = await role_service.get_role(2)
#   res = await user_service.add_user(login='user', password='alek', role=2)
#   res = await user_service.update_user(1, login='user2')
#   res = await user_service.get_user(1)
    res = await user_service.del_user(1)

    print(res)

if __name__ == '__main__':
    asyncio.run(runner())