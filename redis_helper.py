import json
import redis
import pickle

from DemoProject import settings

CACHE_HOST = settings.REDIS_CACHE_HOST
CACHE_PORT = settings.REDIS_CACHE_PORT
CACHE_ENABLED = settings.REDIS_CACHE_ENABLED
CACHE_PASSWORD = settings.REDIS_CACHE_PASSWORD


class RedisCacheManager:
    def __init__(self):
        self.connection: redis.Redis = None

    def connect(self):
        try:
            if self.connection is None:
                # self.connection = redis.StrictRedis()
                self.connection = redis.Redis(host=CACHE_HOST, port=CACHE_PORT, db=0)
        except Exception as ex:
            raise ex

    def get_redis_instance(self):
        try:
            if self.connection is None:
                self.connect()
            return self.connection
        except Exception as ex:
            raise ex

    def object_to_bytes(self, obj):
        try:
            obj_str = json.dumps(obj)
            byt = ' '.join(format(ord(char), 'b') for char in obj_str)
            return byt
        except Exception as ex:
            raise ex

    def bytes_to_obj(self, byt):
        try:
            bytes_str = ''.join(chr(int(x, 2)) for x in byt.split())
            obj = json.loads(bytes_str)
            return obj
        except Exception as ex:
            raise ex

    def has_cache_key(self, key):
        try:
            self.get_redis_instance().exists(key)
            return self.get_redis_instance().exists(key)
        except Exception as ex:
            raise ex

    def put_in_cache(self, key, value):
        try:
            if CACHE_ENABLED:
                return self.get_redis_instance().set(key, self.object_to_bytes(value))
        except Exception as ex:
            raise ex

    def put_obj_in_cache(self, key, obj):
        try:
            if CACHE_ENABLED:
                pickled_obj = pickle.dumps(obj)
                return self.get_redis_instance().set(key, pickled_obj)
        except Exception as ex:
            raise ex

    def get_object_cache(self, key):
        try:
            data_object = self.get_redis_instance().get(key)
            if not data_object is None:
                data_object = pickle.loads(data_object)
            return data_object
        except Exception as ex:
            raise ex

    def get_cache(self, key):
        try:
            if self.has_cache_key(key):
                return self.bytes_to_obj(self.get_redis_instance().get((key)))
        except Exception as ex:
            raise ex

    def invalidate_key(self, key):
        try:
            return self.get_redis_instance().delete(key)
        except Exception as ex:
            raise ex

    def flush_all(self):
        try:
            return self.get_redis_instance().flushall()
        except Exception as ex:
            raise ex

    def delete_key(self, key):
        try:
            return self.get_redis_instance().delete(key)
        except Exception as ex:
            raise ex

    def get_pattern_keys(self, pattern):
        try:
            returned_list = []
            keys = self.get_redis_instance().keys(pattern=pattern)
            values = [self.get_object_cache(key) for key in keys]
            for value in values:
                returned_list.append(value)
            return returned_list
        except Exception as ex:
            raise ex


# from datetime import datetime
# date = datetime.strptime('21-11-2023', "%d-%m-%Y")
# print(date)