from datetime import datetime, timedelta
from core.config.settings import settings
from jose import jwt


class Token:
    @staticmethod
    def access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update(
            {
                "exp": expire,
            }
        )
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt


access_token = Token().access_token
