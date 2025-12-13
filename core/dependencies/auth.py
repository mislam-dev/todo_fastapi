from typing import Union
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, defer
from core.config import settings
from database.database import db_instance
from jose import JWTError, jwt
from core.config.settings import settings
from user.models.user import User


security = HTTPBearer()


class Auth:
    unauthenticated_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def authenticate(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(db_instance.get_db),
    ):

        self.get_current_user(credentials, db)
        return True

    def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(db_instance.get_db),
    ):
        token = credentials.credentials
        payload = self._get_token_data(token)
        user = self._get_user_with_email(db, payload.get("sub"))
        if user is None:
            raise self.unauthenticated_exception

        return user

    # private method
    def _decode_token(self, token: str):
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload

    def _get_token_data(self, token: str):
        data = self._validate_token(token)
        return data

    def _validate_token(self, token):
        token_data = self._decode_token(token)
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")  # type: ignore
            if email is None:
                raise self.unauthenticated_exception
            return payload
        except JWTError:
            raise self.unauthenticated_exception

    def _get_user_with_email(self, db: Session, email: Union[str, None]):
        if email is None:
            return
        return (
            db.query(User)
            .options(defer(User.password))
            .filter(User.email == email)
            .first()
        )


auth = Auth()
