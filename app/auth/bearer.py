from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import get_settings

class BearerAuth(HTTPBearer):

    settings = None

    def __init__(self, auto_error: bool = True):
        super(BearerAuth, self).__init__(auto_error=auto_error)

        self.settings = get_settings()

    async def __call__(self, request):
        credentials: HTTPAuthorizationCredentials = await super(BearerAuth, self).__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token de autenticação não fornecido"
            )
        if credentials.scheme != "Bearer" or not self.verify_token(credentials.credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Token de autenticação inválido"
            )
        return credentials.credentials

    def verify_token(self, token: str) -> bool:
        return token == self.settings.SECRET_KEY