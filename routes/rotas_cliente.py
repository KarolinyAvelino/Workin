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

router = APIRouter(prefix="/cliente")
templates = obter_jinja_templates("templates")


@router.get("/perfil_cliente", response_class=HTMLResponse)
async def get_perfil_cliente(request: Request):
    return templates.TemplateResponse("cliente/pages/perfil_cliente.html", {"request": request})

@router.post("/post_perfil_cliente", response_class=HTMLResponse)
async def post_perfil_cliente(request: Request):
    form_data = await request.form()
    # Aqui você pode processar os dados do formulário
    return templates.TemplateResponse("cliente/pages/perfil_cliente.html", {"request": request})

@router.get("/perfil_prestador", response_class=HTMLResponse)
async def perfil_prestador(request: Request):
    return templates.TemplateResponse("cliente/pages/perfil_prestador.html", {"request": request})

@router.get("/demanda_cliente", response_class=HTMLResponse)
async def get_demanda_cliente(request: Request):
    return templates.TemplateResponse("cliente/pages/demanda_cliente.html", {"request": request})

@router.get("/comentario_cliente", response_class=HTMLResponse)
async def get_comentario_cliente(request: Request):
    return templates.TemplateResponse("cliente/pages/comentario_cliente.html", {"request": request})

@router.get("/editar", response_class=HTMLResponse)
async def get_editar(request: Request):
    return templates.TemplateResponse("cliente/pages/editar.html", {"request": request})

@router.post("/editar", response_class=HTMLResponse)
async def post_editar(request: Request):
    return templates.TemplateResponse("cliente/pages/editar.html", {"request": request})

