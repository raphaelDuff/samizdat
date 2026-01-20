from typing import Callable, TypeVar
from sqlmodel.ext.asyncio.session import AsyncSession


RepoFactory = Callable[[AsyncSession], object]


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        repo_factories: dict[str, RepoFactory],
    ):
        self._session_factory = session_factory
        self._repo_factories = repo_factories

    async def __aenter__(self):
        self.session = self._session_factory()
        for name, factory in self._repo_factories.items():
            setattr(self, name, factory(self.session))

        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
