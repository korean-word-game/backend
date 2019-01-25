import hashlib
import time

from config.settings.base import REDIS_URI, REDIS_INFO
import aioredis
import redis
import asyncio
from contextlib import closing

redis_pool = redis.ConnectionPool(
    host=REDIS_INFO['host'],
    port=REDIS_INFO['port'],
    db=2,
    password=REDIS_INFO['auth'],
    decode_responses=True
)


def get_redis_conn():
    return redis.StrictRedis(
        connection_pool=redis_pool,
        charset="utf-8"
    )


_room_lock = {}


async def get_redis_lock(name):
    if not _room_lock.get(name):
        _room_lock[name] = asyncio.Lock()

    return _room_lock[name]


def get_sha512(p0):
    return hashlib.sha3_512(p0.encode('utf-8')).hexdigest()


def get_token(p0):
    return get_sha512(p0 + ':' + (time.time() * 1000).__int__().__str__())


class AioRedisQuery:
    URI = REDIS_URI + '/2'  # db:2

    @staticmethod
    async def add_user(room_id, username):
        conn = await aioredis.create_redis_pool(AioRedisQuery.URI, encoding='utf-8')
        with closing(conn):
            async with await get_redis_lock(room_id):
                await conn.rpush('room:' + room_id, username)

    @staticmethod
    async def pop_user(room_id, username):
        conn = await aioredis.create_redis_pool(AioRedisQuery.URI, encoding='utf-8')
        with closing(conn):
            async with await get_redis_lock(room_id):
                return await conn.lrem('room:' + room_id, 0, username)

    @staticmethod
    async def exist_user(room_id, username):
        conn = await aioredis.create_redis_pool(AioRedisQuery.URI, encoding='utf-8')
        with closing(conn):
            async with await get_redis_lock(room_id):
                return username in (await conn.lrange('room:' + room_id, 0, -1))

    @staticmethod
    async def room_user_cnt(room_id):
        conn = await aioredis.create_redis_pool(AioRedisQuery.URI, encoding='utf-8')
        with closing(conn):
            async with await get_redis_lock(room_id):
                return await conn.llen('room:' + room_id)

    @staticmethod
    async def get_all_game_config(room_id):
        conn = await aioredis.create_redis_pool(AioRedisQuery.URI, encoding='utf-8')
        with closing(conn):
            return await conn.hgetall('game:' + room_id)

    @staticmethod
    async def get_room_users(room_id):
        conn = await aioredis.create_redis_pool(AioRedisQuery.URI, encoding='utf-8')
        with closing(conn):
            return await conn.lrange('room:' + room_id, 0, -1)

    @staticmethod
    async def set_game_config(room_id, key, value):
        conn = await aioredis.create_redis_pool(AioRedisQuery.URI, encoding='utf-8')
        with closing(conn):
            return await conn.hset('game:' + room_id, key, value)


class RedisQuery:
    @staticmethod
    def add_user(room_id, username):
        conn = get_redis_conn()
        return conn.rpush('room:' + room_id, username)

    @staticmethod
    def pop_user(room_id, username):
        conn = get_redis_conn()
        return conn.lrem('room:' + room_id, 0, username)

    @staticmethod
    def exist_user(room_id, username):
        conn = get_redis_conn()
        return username in conn.lrange('room:' + room_id, 0, -1)

    @staticmethod
    def room_user_cnt(room_id):
        conn = get_redis_conn()
        return conn.llen('room:' + room_id)

    @staticmethod
    def get_room_users(room_id):
        conn = get_redis_conn()
        return conn.lrange('room:' + room_id, 0, -1)

    @staticmethod
    def set_game_config(room_id, key, value):
        conn = get_redis_conn()
        return conn.hset('game:' + room_id, key, value)

    @staticmethod
    def get_game_config(room_id, key):
        conn = get_redis_conn()
        return conn.hget('game:' + room_id, key)

    @staticmethod
    def get_all_game_config(room_id):
        conn = get_redis_conn()
        return conn.hgetall('game:' + room_id)
