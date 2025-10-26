"""Rate limiting using Redis"""

import redis.asyncio as redis

from .config import settings


class RateLimiter:
    """Redis-based rate limiter"""

    def __init__(self) -> None:
        self.redis_client: redis.Redis | None = None
        self.anon_limit = settings.rate_limit_anon
        self.authed_limit = settings.rate_limit_authed

    async def _get_client(self) -> redis.Redis:
        """Get or create Redis client"""
        if self.redis_client is None:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        return self.redis_client

    async def check_rate_limit(self, client_id: str, is_authed: bool) -> bool:
        """Check if client is within rate limit

        Args:
            client_id: Unique client identifier
            is_authed: Whether client is authenticated

        Returns:
            True if within limit, False if exceeded
        """
        try:
            client = await self._get_client()
            key = f"ratelimit:{client_id}"

            # Get current count
            count = await client.get(key)
            current = int(count) if count else 0

            # Check limit
            limit = self.authed_limit if is_authed else self.anon_limit

            if current >= limit:
                return False

            # Increment and set TTL (1 hour)
            pipe = client.pipeline()
            pipe.incr(key)
            pipe.expire(key, 3600)
            await pipe.execute()

            return True

        except Exception:
            # If Redis is down, allow the request (fail open)
            return True

    async def close(self) -> None:
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()


# Singleton instance
rate_limiter = RateLimiter()
