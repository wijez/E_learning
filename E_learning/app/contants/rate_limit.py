from django.core.cache import cache
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status

def rate_limit(key_prefix, limit, timeout):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_key = f"{key_prefix}_{request.user.id}"
            current_count = cache.get(user_key, 0)

            if current_count >= limit:
                return Response({"detail": "Rate limit exceeded. Please try again later."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)

            cache.set(user_key, current_count + 1, timeout)
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
