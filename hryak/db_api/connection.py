import os
import re
import aiomysql
import aiosqlite
from hryak import config

class ConnectionPool:
    def __init__(self):
        self.pool = None
        self.engine = getattr(config, 'DB_ENGINE', 'mysql') or 'mysql'
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.db = None
        self.sqlite_path = None

    def set_config(self, **db_config):
        # Determine engine from config
        self.engine = getattr(config, 'DB_ENGINE', 'mysql') or 'mysql'
        if self.engine == 'sqlite':
            self.sqlite_path = db_config.get('sqlite_path') or getattr(config, 'SQLITE_PATH', 'data/hryak.db')
            # ensure folder exists
            os.makedirs(os.path.dirname(self.sqlite_path) or '.', exist_ok=True)
        else:
            self.host = db_config['host']
            self.port = db_config['port']
            self.user = db_config['user']
            self.password = db_config['password']
            self.db = db_config['database']

    async def create_pool(self):
        if self.engine == 'sqlite':
            # aiosqlite doesn't have a pool; keep connection on pool attr
            self.pool = await aiosqlite.connect(self.sqlite_path)
            await self.pool.execute('PRAGMA journal_mode=WAL;')
            await self.pool.execute('PRAGMA synchronous=NORMAL;')
            await self.pool.commit()
            await self._init_sqlite_schema()
        else:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                autocommit=True,
                maxsize=50,
            )

    async def close(self):
        if self.pool is not None:
            if self.engine == 'sqlite':
                await self.pool.close()
            else:
                self.pool.close()
                await self.pool.wait_closed()

    async def get_connection(self):
        if self.pool is None:
            raise RuntimeError("Connection pool not initialized.")
        if self.engine == 'sqlite':
            return self.pool
        if self.pool._loop.is_closed():
            raise RuntimeError("Event loop is closed.")
        return await self.pool.acquire()

    async def release_connection(self, conn):
        if self.pool is None or conn is None:
            return
        if self.engine == 'sqlite':
            # nothing to do; single shared connection
            return
        try:
            self.pool.release(conn)
        except Exception as e:
            print(f"[Release Error] {e}")

    async def _init_sqlite_schema(self):
        """Create minimal schema for SQLite if not exists."""
        users = f"""
        CREATE TABLE IF NOT EXISTS {config.users_schema} (
            id TEXT PRIMARY KEY,
            created INTEGER DEFAULT 0,
            pig TEXT,
            inventory TEXT,
            stats TEXT,
            events TEXT,
            history TEXT,
            rating TEXT,
            settings TEXT,
            orders TEXT
        );
        """
        shop = f"""
        CREATE TABLE IF NOT EXISTS {config.shop_schema} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            data TEXT
        );
        """
        promocodes = f"""
        CREATE TABLE IF NOT EXISTS {config.promocodes_schema} (
            id TEXT PRIMARY KEY,
            created TEXT,
            users_used TEXT,
            max_uses INTEGER,
            prise TEXT,
            expires_in INTEGER
        );
        """
        guilds = f"""
        CREATE TABLE IF NOT EXISTS {config.guilds_schema} (
            id TEXT PRIMARY KEY,
            joined INTEGER,
            settings TEXT
        );
        """
        async with self.pool.execute(users):
            pass
        async with self.pool.execute(shop):
            pass
        async with self.pool.execute(promocodes):
            pass
        async with self.pool.execute(guilds):
            pass
        await self.pool.commit()


pool = ConnectionPool()


class Connection:

    @staticmethod
    async def make_request(query, params=None, commit=True, fetch=False, fetch_first=True, fetchall=False,
                           executemany=False):
        conn = None
        cur = None
        result = None
        try:
            conn = await pool.get_connection()
            if pool.engine == 'sqlite':
                # adapt query from MySQL style to SQLite
                q = query
                # Handle CONCAT(...) -> (arg1 || arg2 || ...)
                def _rewrite_concat(sql: str) -> str:
                    pattern = re.compile(r'CONCAT\s*\(([^)]*)\)', re.IGNORECASE)
                    def repl(m):
                        args = m.group(1)
                        # split by commas that are not inside quotes
                        parts = []
                        buf = ''
                        in_quote = False
                        for ch in args:
                            if ch == "'":
                                in_quote = not in_quote
                                buf += ch
                            elif ch == ',' and not in_quote:
                                parts.append(buf.strip())
                                buf = ''
                            else:
                                buf += ch
                        if buf.strip():
                            parts.append(buf.strip())
                        return '(' + ' || '.join(parts) + ')'
                    return pattern.sub(repl, sql)
                q = _rewrite_concat(q)
                # placeholders
                if params is not None:
                    q = q.replace('%s', '?')
                # JSON functions
                q = re.sub(r'JSON_EXTRACT', 'json_extract', q, flags=re.IGNORECASE)
                q = re.sub(r'JSON_INSERT', 'json_insert', q, flags=re.IGNORECASE)
                # Remove JSON_UNQUOTE wrappers around json_extract: JSON_UNQUOTE(json_extract(...)) -> json_extract(...)
                q = re.sub(r'JSON_UNQUOTE\s*\(\s*json_extract\s*\((.*?)\)\s*\)', r'json_extract(\1)', q, flags=re.IGNORECASE)
                # Replace DECIMAL casts with REAL
                q = re.sub(r'CAST\s*\((.*?)\s+AS\s+DECIMAL\s*\([^\)]*\)\)', r'CAST(\1 AS REAL)', q, flags=re.IGNORECASE)
                # INSERT IGNORE INTO -> INSERT OR IGNORE INTO
                q = re.sub(r'^\s*INSERT\s+IGNORE\s+INTO', 'INSERT OR IGNORE INTO', q, flags=re.IGNORECASE)
                # JSON_CONTAINS_PATH(json, 'one', '$."%s"') = 1  -> json_type(json, '$.' || ?) IS NOT NULL
                q = re.sub(r"JSON_CONTAINS_PATH\s*\(([^,]+),\s*'one'\s*,\s*'\$\\\.\\\"%s\\\"'\s*\)\s*=\s*1",
                           r"json_type(\1, '$.' || ?) IS NOT NULL", q, flags=re.IGNORECASE)
                # Remove MySQL-specific ALTERs silently by short-circuiting
                if q.strip().upper().startswith('ALTER TABLE'):
                    return None
                cur = await conn.cursor()
                if executemany:
                    await cur.executemany(q, params or [])
                else:
                    await cur.execute(q, params or [])
            else:
                cur = await conn.cursor()
                if executemany:
                    await cur.executemany(query, params)
                else:
                    await cur.execute(query, params)

            print(query, result)
            if fetch:
                if pool.engine == 'sqlite':
                    if fetchall or not fetch_first:
                        rows = await cur.fetchall()
                        result = rows
                    else:
                        row = await cur.fetchone()
                        result = row
                else:
                    result = await cur.fetchall() if fetchall or not fetch_first else await cur.fetchone()

            if fetch_first and not fetchall:
                result = result[0] if result else None

            if commit:
                if pool.engine == 'sqlite':
                    await conn.commit()
                else:
                    await conn.commit()

            return result



        except Exception as e:
            print(e)
            if conn:
                try:
                    await conn.rollback()
                except Exception:
                    pass
                if pool.engine != 'sqlite':
                    await conn.ensure_closed()
            raise e

        finally:
            print(result)
            if cur:
                await cur.close()
            if conn:
                await pool.release_connection(conn)