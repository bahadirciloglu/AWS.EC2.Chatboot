from fastapi import Request

async def context_middleware(request: Request, call_next):
    user_id = request.headers.get("X-User-Id") or "anonymous"
    request.state.user_id = user_id
    response = await call_next(request)
    return response
