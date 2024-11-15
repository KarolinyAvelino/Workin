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

from fastapi import FastAPI
from routes.rotas_prestador import router as rotas_prestador

app = FastAPI()

# Registre as rotas
app.include_router(rotas_prestador)

router = APIRouter()
templates = obter_jinja_templates("templates")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario or not usuario.perfil:
        return templates.TemplateResponse("main/pages/login.html", {"request": request})    
    if usuario.perfil == 1:
        return RedirectResponse("/perfil_cliente", status_code=status.HTTP_303_SEE_OTHER)
    if usuario.perfil == 2:
        return RedirectResponse("/perfil_prestador", status_code=status.HTTP_303_SEE_OTHER)
    if usuario.perfil == 3:
        return RedirectResponse("/perfil_admin", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/post_login", response_class=HTMLResponse)
async def post_login(
    email: str = Form(...),
    senha: str = Form(...)):
    # busca o usuário dono deste email
    usuario = UsuarioRepo.checar_credenciais(email, senha)
    # se não encontrou o usuário, é porque não existe um usuário com este e-mail
    if not usuario:
        response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Credenciais inválidas! Cheque os valores digitados a tente novamente.")
        return response
    # se encontrou, confere a senha digitada com a senha que veio do banco de dados
        # se a senha confere, cria o token com os dados do usuário e seu perfil
    token = criar_token(usuario[0], usuario[1], usuario[2], usuario[3])
    # captura o nome do perfil de acordo com o número gravado no banco de dados
    nome_perfil = None
    match (usuario[2]):
        case 1: nome_perfil = "perfil_cliente"
        case 2: nome_perfil = "perfil_prestador"
        case 3: nome_perfil = "perfil_admin"
        case _: nome_perfil = ""        
    # cria uma respostas de redirecionamento para a área restrita do perfil
    response = RedirectResponse(f"/{nome_perfil}", status_code=status.HTTP_303_SEE_OTHER) 
    # grava na resposta o cookie contendo o token de autenticação   
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=3600*24*365*10,
        httponly=True,
        samesite="lax"
    )
    # grava na resposta uma mensagem de sucesso do login
    adicionar_mensagem_sucesso(response, "Login realizado com sucesso!")
    # envia a resposta para o usuário
    return response
# se a senha não confere

@router.get("/redefinir_senha", response_class=HTMLResponse)
async def get_redefinir_senha(request: Request):
    return templates.TemplateResponse("main/pages/redefinir_senha.html", {"request": request})

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
    return RedirectResponse("/reenviar_codigo", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/barra_pesquisa", response_class=HTMLResponse)
async def get_barra_pesquisa(request: Request):
    return templates.TemplateResponse("main/pages/barra_pesquisa.html", {"request": request})

@router.get("/reenviar_codigo", response_class=HTMLResponse)
async def get_reenviar_codigo(request: Request):
    return templates.TemplateResponse("main/pages/reenviar_codigo.html", {"request": request})

@router.post("/post_reenviar_codigo")
async def post_reenviar_codigo(
    request: Request, 
    codigo: str = Form(...),    
    nova_senha: str = Form(...),
    conf_nova_senha: str = Form(...)):
    id_usuario = request.state.usuario.id
    usuario = UsuarioRepo.obter_por_id(id_usuario)    
    if nova_senha == conf_nova_senha and conferir_senha(codigo,nova_senha,conf_nova_senha, usuario.senha):
        UsuarioRepo.atualizar_senha(id_usuario, obter_hash_senha(nova_senha))
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/suporte", response_class=HTMLResponse)
async def get_suporte(request: Request):
    return templates.TemplateResponse("main/pages/suporte.html", {"request": request})

@router.get("/cadastro_cliente", response_class=HTMLResponse)
async def get_cadastro_cliente(request: Request):
    return templates.TemplateResponse("main/pages/cadastro_cliente.html", {"request": request})

@router.post("/post_cadastro_cliente", response_class=HTMLResponse)
async def post_cadastro_cliente(
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confirma_senha: str = Form(...)):
    if senha != confirma_senha:
        return RedirectResponse("/cadastro_cliente", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(
        nome=nome, 
        email=email, 
        telefone=telefone,
        senha=senha_hash,
        perfil=1)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/perfil_cliente", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/cadastro_prestador", response_class=HTMLResponse)
async def get_cadastro_prestador(request: Request):
    categorias = [
        {"value": 1, "label": "Limpeza"},
        {"value": 2, "label": "Passeador de Pets"},
        {"value": 3, "label": "Beleza"},
    ]
    return templates.TemplateResponse("main/pages/cadastro_prestador.html", {"request": request,"categorias": categorias})

@router.post("/post_cadastro_prestador", response_class=HTMLResponse)
async def post_cadastro_prestador(
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    categoria: str = Form(...),
    especialidade: str = Form(...),
    senha: str = Form(...),
    confirma_senha: str = Form(...)):
    if senha != confirma_senha:
        return RedirectResponse("/cadastro_prestador", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(
        nome=nome, 
        email=email, 
        telefone=telefone, 
        categoria=categoria, 
        especialidade=especialidade, 
        senha=senha_hash, 
        perfil=2)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/prestador/planos", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/404")
async def get_not_found(request: Request):
    return templates.TemplateResponse("pages/404.html", {"request": request})

@router.get("/perfil_cliente", response_class=HTMLResponse)
async def get_perfil_cliente(request: Request):
    return templates.TemplateResponse("cliente/pages/perfil_cliente.html", {"request": request})

@router.get("/sair")
async def get_sair():
    response = RedirectResponse("/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value="",
        max_age=1,
        httponly=True,
        samesite="lax")
    return response

