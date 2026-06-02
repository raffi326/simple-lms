from functools import wraps
from django.core.cache import cache
from ninja.errors import HttpError
import time

def ratelimit(limit=60, period=60):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Use IP address or User ID for identification
            user_id = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
            key = f"ratelimit_{user_id}_{func.__name__}"
            
            # Simple fixed window rate limiting
            current_count = cache.get(key, 0)
            if current_count >= limit:
                raise HttpError(429, "Too many requests. Please try again later.")
            
            cache.set(key, current_count + 1, timeout=period)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
