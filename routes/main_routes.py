from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})

@router.get("/cadastro_prestador", response_class=HTMLResponse)
async def get_cadastro_prestador(request: Request):
    return templates.TemplateResponse("pages/cadastro_prestador.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.get("/redefinir_senha", response_class=HTMLResponse)
async def get_redefinir(request: Request):
    return templates.TemplateResponse("pages/redefinir_senha.html", {"request": request})


@router.get("/perfil_cliente_vc", response_class=HTMLResponse)
async def get_perfil_cliente(request: Request):
    return templates.TemplateResponse("pages/perfil_cliente_vc.html", {"request": request})

@router.get("/perfil_prestador_vc", response_class=HTMLResponse)
async def get_perfil_prestador(request: Request):
    return templates.TemplateResponse("pages/perfil_prestador_vc.html", {"request": request})

@router.get("/barra_pesquisa", response_class=HTMLResponse)
async def get_barra_pesquisa(request: Request):
    return templates.TemplateResponse("pages/barra_pesquisa.html", {"request": request})

@router.get("/reenviar_codigo", response_class=HTMLResponse)
async def get_reenviar_codigo(request: Request):
    return templates.TemplateResponse("pages/reenviar_codigo.html", {"request": request})

@router.get("/cadastro_cliente", response_class=HTMLResponse)
async def get_cadastro_cliente(request: Request):
    return templates.TemplateResponse("pages/cadastro_cliente.html", {"request": request})

@router.get("/suporte", response_class=HTMLResponse)
async def get_suporte(request: Request):
    return templates.TemplateResponse("pages/suporte.html", {"request": request})


@router.get("/dados_cartao", response_class=HTMLResponse)
async def get_dados_cartao(request: Request):
    return templates.TemplateResponse("pages/dados_cartao.html", {"request": request})

@router.get("/demanda_cliente", response_class=HTMLResponse)
async def get_demanda_cliente(request: Request):
    return templates.TemplateResponse("pages/demanda_cliente.html", {"request": request})

@router.get("/denuncia", response_class=HTMLResponse)
async def get_denuncia(request: Request):
    return templates.TemplateResponse("pages/denuncia.html", {"request": request})

@router.get("/demanda_prestador", response_class=HTMLResponse)
async def get_demanda_prestador(request: Request):
    return templates.TemplateResponse("pages/demanda_prestador.html", {"request": request})


@router.get("/prestador_visao_cliente", response_class=HTMLResponse)
async def get_prestador_visao_cliente(request: Request):
    return templates.TemplateResponse("pages/prestador_visao_cliente.html", {"request": request})


@router.get("/suporte_adm", response_class=HTMLResponse)
async def get_suporte_adm(request: Request):
    return templates.TemplateResponse("pages/suporte_adm.html", {"request": request})


@router.get("/comentario_prestador", response_class=HTMLResponse)
async def get_comentario_prestador(request: Request):
    return templates.TemplateResponse("pages/comentario_prestador.html", {"request": request})

@router.get("/editar_cliente", response_class=HTMLResponse)
async def get_editar_cliente(request: Request):
    return templates.TemplateResponse("pages/editar_cliente.html", {"request": request})