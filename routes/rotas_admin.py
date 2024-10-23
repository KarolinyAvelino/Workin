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

router = APIRouter(prefix="/admin")
templates = obter_jinja_templates("templates")


@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("admin/pages/index.html", {"request": request})


@router.get("/denuncia", response_class=HTMLResponse)
async def get_denuncia(request: Request):
    return templates.TemplateResponse("admin/pages/denuncia.html", {"request": request})

@router.get("/suporte", response_class=HTMLResponse)
async def get_suporte_adm(request: Request):
    return templates.TemplateResponse("admin/pages/suporte.html", {"request": request})

@router.get("/categorias", response_class=HTMLResponse)
async def get_categorias_adm(request: Request):
    return templates.TemplateResponse("admin/pages/categorias.html", {"request": request})