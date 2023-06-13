from decouple import config

REDIS_HOST = config("REDIS_HOST", "localhost")
REDIS_PORT = config("REDIS_PORT", 6379)
REDIS_AUTH = config("REDIS_AUTH")
JWT_SECRET = config("JWT_SECRET")
JWT_DOMAIN = config("JWT_DOMAIN", "localhost")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 600)  # 10*60 second =  minutes
JWT_ALGORITHM = config("JWT_ALGORITHM", "HS256")
AUTH_CHALLENGE_SIZE = config("AUTH_CHALLENGE_SIZE", 128)  # size in bytes
AUTH_CHALLENGE_TIMEOUT_IN_SEC = config("AUTH_CHALLENGE_TIMEOUT_IN_SEC", 60)  # timeout in seconds
