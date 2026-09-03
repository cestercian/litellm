from fastapi import HTTPException

from litellm.proxy._types import ProxyException, UserAPIKeyAuth, user_api_key_has_admin_view


def assert_caller_can_list_shared_provider_batches(user_api_key_dict: UserAPIKeyAuth) -> None:
    """Raise 403 unless the caller is allowed to list against shared provider credentials.

    Virtual keys must not enumerate the proxy's shared provider project. Proxy admins
    keep the operator pass-through used when managed batch listing is unavailable.
    """
    if user_api_key_has_admin_view(user_api_key_dict):
        return
    raise HTTPException(
        status_code=403,
        detail="Access denied: listing batches against shared provider credentials is not allowed for this key.",
    )


def validate_batch_list_limit(limit: int | None) -> None:
    if limit is None or 0 <= limit <= 100:
        return
    bound, expected, openai_code = (
        ("below minimum", ">= 0", "integer_below_min_value")
        if limit < 0
        else ("above maximum", "<= 100", "integer_above_max_value")
    )
    raise ProxyException(
        message=f"Invalid 'limit': integer {bound} value. Expected a value {expected}, but got {limit} instead.",
        type="invalid_request_error",
        param="limit",
        code=400,
        openai_code=openai_code,
    )
