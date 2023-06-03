from uuid import uuid4
import redis


class AppConfig:
    JWT_SECERT_KEY = uuid4().hex
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60
    JWT_REFRESH_TOKEN_EXPIRES = 60 * 60 * 2
    SECRET_KEY = uuid4().hex
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_COOKIE_MAX_AGE = 12 * 60 * 60
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")

