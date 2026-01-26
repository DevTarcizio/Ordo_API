from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from ordo_fast.settings import Settings

engine = create_async_engine(
    Settings().DATABASE_URL,  # type: ignore
    pool_size=5,
    max_overflow=0,
    pool_pre_ping=True,
)


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


# Adicionado para evitar travamentos do terminal
async def close_engine():
    await engine.dispose()
