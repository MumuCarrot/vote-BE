from fastapi import Request


def get_request_id(request: Request) -> str:
    """
    Extract request ID from request state.
    """
    return getattr(request.state, "request_id", "unknown")
