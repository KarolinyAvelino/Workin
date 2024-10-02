import datetime
import os
from typing import Optional
import bcrypt
import jwt
from fastapi import HTTPException, Request, status
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.cookies import NOME_COOKIE_AUTH, adicionar_cookie_auth

async def obter_usuario_logado(request: Request) -> Optional[Usuario]:
    try:
        token = request.cookies[NOME_COOKIE_AUTH]
        if token.strip() == "":
            return None
        usuario = UsuarioRepo.obter_por_token(token)
        return usuario
    except KeyError:
        return None


async def middleware_autenticacao(request: Request, call_next):
    usuario = await obter_usuario_logado(request)
    request.state.usuario = usuario
    response = await call_next(request)
    if response.status_code == status.HTTP_303_SEE_OTHER:
        return response
    if usuario:
        token = request.cookies[NOME_COOKIE_AUTH]
        adicionar_cookie_auth(response, token)
    return response


async def checar_permissao(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    area_do_usuario = request.url.path.startswith("/usuario")
    area_do_admin = request.url.path.startswith("/admin")    
    if (area_do_usuario or area_do_admin) and (not usuario or not usuario.perfil):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if area_do_usuario and usuario.perfil != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if area_do_admin and usuario.perfil != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

def obter_hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""


def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False
    
def criar_token(id: int, nome: str, email: str, perfil: int) -> str:
    payload = {
        "id": id,
        "nome": nome,
        "email": email,
        "perfil": perfil,
        "exp": datetime.now() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, 
        os.getenv("JWT_SECRET"),
        os.getenv("JWT_ALGORITHM"))


def validar_token(token: str) -> dict:
    try:
        return jwt.decode(token, 
            os.getenv("JWT_SECRET"),
            os.getenv("JWT_ALGORITHM"))
    except jwt.ExpiredSignatureError:
        return { id: None, "nome": None, "email": None, "perfil": None, "mensagem": "Token expirado" }
    except jwt.InvalidTokenError:
        return { id: None, "nome": None, "email": None, "perfil": None, "mensagem": "Token inválido" }
    except Exception as e:
        return { id: None, "nome": None, "email": None, "perfil": None, "mensagem": f"Erro: {e}" }
    

def criar_cookie_auth(response, token):
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=1800,
        httponly=True,
        samesite="lax",
    )
    return response
