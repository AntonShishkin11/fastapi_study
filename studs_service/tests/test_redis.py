import pytest

from cache_redis.redis_service import set_cache, get_cache, delete_cache

#Для тестирования редис локально, нужно в .env указать REDIS_HOST=localhost

class TestRedis:

    @pytest.mark.parametrize('a, b', [
        (1, 1),
        (2, 2),
        (4, 4)
    ])
    def test_testing(self, a, b):
        assert a == b

    @pytest.mark.parametrize('key, value', [
        ('simple_key', {'a': 1}),
        ('empty_dict', {}),
        ('k' * 1000, {'bigkey': True}),
        ('ключ', {'значение': '🧠'}),
        ('nested', {'outer': {'inner': [1, 2, 3]}}),
        ('bools', {'flag': True, 'other': None}),
        ('mixed', {'int': 42, 'float': 3.14, 'str': 'ok'}),
        ('weird!@#$%^&*()_+=', {'data': 'value'}),
    ])
    @pytest.mark.asyncio(loop_scope='session')
    async def test_redis_cache(self, key, value):
        await set_cache(key, value, ex=10)

        cached_value = await get_cache(key)
        assert cached_value == value

        await delete_cache(key)
        deleted_value = await get_cache(key)
        assert deleted_value is None
