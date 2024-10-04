from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from Workin.util.auth import conferir_senha, obter_hash_senha
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import criar_token
from util.cookies import NOME_COOKIE_AUTH
from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})

@router.get("/cadastro_prestador", response_class=HTMLResponse)
async def get_cadastro_prestador(request: Request):
    return templates.TemplateResponse("pages/cadastro_prestador.html", {"request": request})

@router.get("/cadastro_cliente", response_class=HTMLResponse)
async def get_cadastro_cliente(request: Request):
    return templates.TemplateResponse("pages/cadastro_cliente.html", {"request": request})

@router.post("/post_cadastro_prestador", response_class=HTMLResponse)
async def post_cadastro_prestador(
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    categoria: str = Form(...),
    especialidade: str = Form(...),
    senha: str = Form(...),
    confirmaSenha: str = Form(...),
    perfil: int = Form(...)):
    if senha != confirmaSenha:
        return RedirectResponse("/post_cadastro_prestador", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(None, nome, email, telefone, categoria, especialidade, senha_hash, None, perfil)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/post_cadastro_cliente", response_class=HTMLResponse)
async def post_cadastro_cliente(
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confirmaSenha: str = Form(...),
    perfil: int = Form(...)):
    if senha != confirmaSenha:
        return RedirectResponse("/post_cadastro_prestador", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(None, nome, email, telefone, senha_hash, None, perfil)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.post("/post_login", response_class=HTMLResponse)
async def post_login(
    email: str = Form(...),
    senha: str = Form(...)):
    usuario = UsuarioRepo.obter_por_email(email)
    if not usuario:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    if conferir_senha(senha, usuario.senha):
        token = criar_token(usuario.id, usuario.nome, usuario.email, usuario.perfil, usuario.telefone, usuario.categoria, usuario.especialidade, usuario.id,)
        nome_perfil = None
        match (usuario.perfil):
            case 1: nome_perfil = "cliente"
            case 2: nome_perfil = "prestador"
            case _: nome_perfil = ""
        
        response = RedirectResponse(f"/{nome_perfil}", status_code=status.HTTP_303_SEE_OTHER)    
        response.set_cookie(
            key=NOME_COOKIE_AUTH,
            value=token,
            max_age=3600*24*365*10,
            httponly=True,
            samesite="lax"
        )
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/redefinir_senha", response_class=HTMLResponse)
async def get_redefinir(request: Request):
    return templates.TemplateResponse("pages/redefinir_senha.html", {"request": request})

@router.post("/post_redefinir_senha")
async def post_redefinir_senha(
    request: Request, 
    senha_atual: str = Form(...),    
    nova_senha: str = Form(...),
    conf_nova_senha: str = Form(...)):
    id_usuario = request.state.usuario.id
    usuario = UsuarioRepo.obter_por_id(id_usuario)    
    if nova_senha == conf_nova_senha and conferir_senha(senha_atual, usuario.senha):
        UsuarioRepo.atualizar_senha(id_usuario, obter_hash_senha(nova_senha))
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/perfil_cliente_vc", response_class=HTMLResponse)
async def get_perfil_cliente(request: Request):
    return templates.TemplateResponse("pages/perfil_cliente_vc.html", {"request": request})

@router.get("/perfil_prestador_vc", response_class=HTMLResponse)
async def get_perfil_prestador_vc(request: Request):
    return templates.TemplateResponse("pages/perfil_prestador_vc.html", {"request": request})

@router.get("/barra_pesquisa", response_class=HTMLResponse)
async def get_barra_pesquisa(request: Request):
    return templates.TemplateResponse("pages/barra_pesquisa.html", {"request": request})

@router.get("/reenviar_codigo", response_class=HTMLResponse)
async def get_reenviar_codigo(request: Request):
    return templates.TemplateResponse("pages/reenviar_codigo.html", {"request": request})

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

@router.get("/planos", response_class=HTMLResponse)
async def get_planos(request: Request):
    return templates.TemplateResponse("pages/planos.html", {"request": request})


@router.get("/categorias_adm", response_class=HTMLResponse)
async def get_categorias_adm(request: Request):
    return templates.TemplateResponse("pages/categorias_adm.html", {"request": request})

