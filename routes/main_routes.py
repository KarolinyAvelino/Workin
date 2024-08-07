from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})

@router.get("/cadastro", response_class=HTMLResponse)
async def get_cadastro(request: Request):
    return templates.TemplateResponse("pages/cadastro.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.get("/redefinir_senha", response_class=HTMLResponse)
async def get_redefinir(request: Request):
    return templates.TemplateResponse("pages/redefinir_senha.html", {"request": request})
