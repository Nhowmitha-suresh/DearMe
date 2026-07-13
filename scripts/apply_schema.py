import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine


async def main():
    # prefer DATABASE_URL env var, fallback to app config if available
    url = os.getenv('DATABASE_URL')
    if not url:
        try:
            from app.core.config import settings

            url = settings.DATABASE_URL
        except Exception:
            url = None

    if not url:
        print('No DATABASE_URL found in environment or app.core.config')
        raise SystemExit(1)

    print('Using DATABASE_URL:', url)
    engine = create_async_engine(url, future=True)
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'schema.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    async with engine.begin() as conn:
        print('Applying schema...')
        raw_conn = await conn.get_raw_connection()
        await raw_conn.driver_connection.execute(sql)
    await engine.dispose()
    print('Schema applied successfully')


if __name__ == '__main__':
    asyncio.run(main())
