from fastapi import Depends, HTTPException, Header
from services.token_service import decode_token

async def get_current_user(user_token: str = Header(...)):
    payload = decode_token(user_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["sub"]
