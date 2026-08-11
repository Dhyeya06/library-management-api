from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)

        if not payload.get("sub"):
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )