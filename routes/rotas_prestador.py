from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth import conferir_senha, obter_hash_senha
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import criar_token
from util.cookies import NOME_COOKIE_AUTH
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/prestador")
templates = obter_jinja_templates("templates")


@router.get("/planos", response_class=HTMLResponse)
async def get_planos(request: Request):
    return templates.TemplateResponse("prestador/pages/planos.html", {"request": request})

@router.post("/post_planos")
async def post_planos(request: Request, plano: str = Form(...)):
    if plano == "gratuito":
        return RedirectResponse("/perfil_prestador", status_code=status.HTTP_303_SEE_OTHER)
    elif plano == "pago":
        return RedirectResponse("/dados_cartao", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/dados_cartao", response_class=HTMLResponse)
async def get_dados_cartao(request: Request):
    return templates.TemplateResponse("prestador/pages/dados_cartao.html", {"request": request})

@router.get("/demanda_prestador", response_class=HTMLResponse)
async def get_demanda_prestador(request: Request):
    return templates.TemplateResponse("prestador/pages/demanda_prestador.html", {"request": request})

@router.get("/comentario_prestador", response_class=HTMLResponse)
async def get_comentario_prestador(request: Request):
    return templates.TemplateResponse("prestador/pages/comentario_prestador.html", {"request": request})

@router.get("/editar_prestador", response_class=HTMLResponse)
async def get_editar_prestador(request: Request):
    return templates.TemplateResponse("prestador/pages/editar_prestador.html", {"request": request})

@router.get("/encerrar_plano", response_class=HTMLResponse)
async def get_encerrar_plano(request: Request):
    return templates.TemplateResponse("prestador/pages/encerrar_plano.html", {"request": request})

@router.get("/perfil_cliente", response_class=HTMLResponse)
async def get_perfil_cliente(request: Request):
    return templates.TemplateResponse("prestador/pages/perfil_cliente.html", {"request": request})

@router.get("/perfil_prestador", response_class=HTMLResponse)
async def get_perfil_prestador(request: Request):
    return templates.TemplateResponse("prestador/pages/perfil_prestador.html", {"request": request})