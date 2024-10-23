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

router = APIRouter()
templates = obter_jinja_templates("templates")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/index.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("main/pages/login.html", {"request": request})

@router.post("/post_login", response_class=HTMLResponse)
async def post_login(
    email: str = Form(...),
    senha: str = Form(...)):
    # busca o usuário dono deste email
    usuario = UsuarioRepo.obter_por_email(email)
    # se não encontrou o usuário, é porque não existe um usuário com este e-mail
    if not usuario:
        response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Credenciais inválidas! Cheque os valores digitados a tente novamente.")
        return response
    # se encontrou, confere a senha digitada com a senha que veio do banco de dados
    if conferir_senha(senha, usuario.senha):
        # se a senha confere, cria o token com os dados do usuário e seu perfil
        token = criar_token(usuario.id, usuario.nome, usuario.email, usuario.perfil)
        # captura o nome do perfil de acordo com o número gravado no banco de dados
        nome_perfil = None
        match (usuario.perfil):
            case 1: nome_perfil = "cliente"
            case 2: nome_perfil = "prestador"
            case 3: nome_perfil = "admin"
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
    else:
        # cria uma resposta para a própria página de login
        response = RedirectResponse("/login", status. HTTP_303_SEE_OTHER)
        # grava uma mensagem negativa nessa resposta
        adicionar_mensagem_erro(response, "Credenciais inválidas! Cheque os valores digitados a tente novamente.")
        # envia a resposta para o usuário
        return response

@router.get("/redefinir_senha", response_class=HTMLResponse)
async def get_redefinir(request: Request):
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
    return templates.TemplateResponse("main/pages/cadastro_prestador.html", {"request": request})

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
    return RedirectResponse("/planos", status_code=status.HTTP_303_SEE_OTHER)