from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Optional


class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None

    @property
    def session(self) -> AsyncSession:
        assert self._session is not None, "Session accessed outside UoW context"
        return self._session

    async def __aenter__(self):
        self._session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        assert self._session is not None
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
        self._session = None

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
