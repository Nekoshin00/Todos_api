from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import dominio.db_model as models
from config import DIR_DB
from utils.generic_utils import create_db_directory

URL = f"sqlite+aiosqlite:///{DIR_DB}/db.sqlite"

engine = create_async_engine(url=URL, echo=False, future=True)
local_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with local_session() as session:
        yield session

async def create_db():
    result = create_db_directory()
    if result:
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)