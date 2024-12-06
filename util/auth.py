from datetime import datetime
from datetime import timedelta
import os
import bcrypt
from fastapi import HTTPException, Request, status
import jwt
from dtos.usuario_autenticado_dto import UsuarioAutenticadoDto
from util.cookies import NOME_COOKIE_AUTH

async def obter_usuario_logado(request: Request) -> dict:
    try:
        token = request.cookies[NOME_COOKIE_AUTH]
        if token.strip() == "":
            return None
        dados = validar_token(token)
        usuario = UsuarioAutenticadoDto(
            id = int(dados["id"]),
            nome = dados["nome"], 
            email = dados["email"], 
            perfil= dados["perfil"])
        if "mensagem" in dados.keys():
            usuario.mensagem = dados["mensagem"]
        return usuario
    except KeyError:
        return None


async def checar_autenticacao(request: Request, call_next):
    usuario = await obter_usuario_logado(request)
    request.state.usuario = usuario
    response = await call_next(request)
    if response.status_code == status.HTTP_303_SEE_OTHER:
        return response
    return response


async def checar_permissao(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    area_do_usuario = request.url.path.startswith("/usuario")
    area_do_admin = request.url.path.startswith("/perfil_admin")
    area_do_cliente = request.url.path.startswith("/perfil_cliente")
    area_do_prestador = request.url.path.startswith("/perfil_prestador")    
    if (area_do_cliente or area_do_usuario or area_do_admin or area_do_prestador) and (not usuario or not usuario.perfil):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if area_do_cliente and usuario.perfil != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if area_do_prestador and usuario.perfil != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if area_do_admin and usuario.perfil != 3:
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
        "exp": datetime.now() + timedelta(days=1)
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

def configurar_swagger_auth(app):
    app.openapi_schema = app.openapi()
    app.openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema["security"] = [{"BearerAuth": []}]