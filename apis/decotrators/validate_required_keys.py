from functools import wraps
from utils import validate_dict_keys
from exceptions import RequiredKeyNotExistError


def validate_required_keys(required_keys):
    # POST 요청 값에서 필수키 값이 있는지 검사.
    # 모든 키가 존재하면 통과 그렇지 않으면, error raise
    def decorator(api_func):
        @wraps(api_func)
        def _wrapped_view(request, *args, **kwargs):
            excluded_keys = validate_dict_keys(required_keys, request.data)
            if len(excluded_keys):
                raise RequiredKeyNotExistError(excluded_keys)
            return api_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
