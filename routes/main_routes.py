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

@router.get("/suporte_adm", response_class=HTMLResponse)
async def get_suporte_adm(request: Request):
    return templates.TemplateResponse("pages/suporte_adm.html", {"request": request})


@router.get("/comentario_prestador", response_class=HTMLResponse)
async def get_comentario_prestador(request: Request):
    return templates.TemplateResponse("pages/comentario_prestador.html", {"request": request})

@router.get("/comentario_cliente", response_class=HTMLResponse)
async def get_comentario_cliente(request: Request):
    return templates.TemplateResponse("pages/comentario_cliente.html", {"request": request})

@router.get("/editar_cliente", response_class=HTMLResponse)
async def get_editar_cliente(request: Request):
    return templates.TemplateResponse("pages/editar_cliente.html", {"request": request})

@router.get("/editar_prestador", response_class=HTMLResponse)
async def get_editar_prestador(request: Request):
    return templates.TemplateResponse("pages/editar_prestador.html", {"request": request})

@router.get("/encerrar_plano", response_class=HTMLResponse)
async def get_encerrar_plano(request: Request):
    return templates.TemplateResponse("pages/encerrar_plano.html", {"request": request})

@router.get("/perfil_cliente_vp", response_class=HTMLResponse)
async def get_perfil_cliente_vp(request: Request):
    return templates.TemplateResponse("pages/perfil_cliente_vp.html", {"request": request})

@router.get("/perfil_prestador_vp", response_class=HTMLResponse)
async def get_perfil_prestador_vp(request: Request):
    return templates.TemplateResponse("pages/perfil_prestador_vp.html", {"request": request})


@router.get("/cliente_responde", response_class=HTMLResponse)
async def get_cliente_responde(request: Request):
    return templates.TemplateResponse("pages/cliente_responde.html", {"request": request})


@router.get("/denuncias_anteriores", response_class=HTMLResponse)
async def get_denuncias_anteriores(request: Request):
    return templates.TemplateResponse("pages/denuncias_anteriores.html", {"request": request})

@router.get("/planos", response_class=HTMLResponse)
async def get_planos(request: Request):
    return templates.TemplateResponse("pages/planos.html", {"request": request})


