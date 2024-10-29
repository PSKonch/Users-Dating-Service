from typing import Annotated

from fastapi import Depends, HTTPException, Request

from src.services.auth import AuthService


def get_token(request: Request):
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        raise HTTPException(status_code=401, detail='Вы не аутентифицированы')
    return access_token

def get_current_client_id(token: Annotated[str, Depends(get_token)]) -> int:
    decoded_token = AuthService().decode_token(token)
    return decoded_token['client_id']

ClientIdDependency = Annotated[int, Depends(get_current_client_id)]