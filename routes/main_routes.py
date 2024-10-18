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




@router.get("/cadastro_prestador", response_class=HTMLResponse)
async def get_cadastro_prestador(request: Request):
    return templates.TemplateResponse("main/pages/cadastro_prestador.html", {"request": request})

@router.get("/cadastro_cliente", response_class=HTMLResponse)
async def get_cadastro_cliente(request: Request):
    return templates.TemplateResponse("main/pages/cadastro_cliente.html", {"request": request})

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
    return RedirectResponse("/perfil_cliente_vc", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/planos", response_class=HTMLResponse)
async def get_planos(request: Request):
    planos = [
        {
            "nome": "Plano Gratuito",
            "preco": "R$0,00",
            "descricao": "RECURSOS LIMITADOS",
            "recursos": [
                "✔ Limite de 3 Fotos",
                "✔ Agenda de Serviços",
                "✔ Feedback",
                "✔ Sistema de Mensagens",
                "✔ Avaliações e Comentários",
                "✖ Suporte",
                "✖ Fotos Ilimitadas",
                "✖ Maior Visibilidade",
                "✖ Análises e Relatórios",
                "✖ Visualização de Ofertas Locais"
            ],
            "link": "/perfil_prestador_vp"  
        },
        {
            "nome": "Plano Pago + 1 mês grátis",
            "preco": "R$29,99",
            "descricao": "por mês",
            "recursos": [
                "✔ Maior Visibilidade",
                "✔ Fotos Ilimitadas",
                "✔ Destaque em Outros Perfis",
                "✔ Agenda de Serviços",
                "✔ Feedback",
                "✔ Análises e Relatórios",
                "✔ Perfil Verificado",
                "✔ Suporte",
                "✔ Visualização de Ofertas Locais",
                "✔ Prioridade nas Solicitações"
            ],
            "link": "/dados_cartao"
        }
    ]

    return templates.TemplateResponse("main/pages/planos.html", {"request": request, "planos": planos})

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("main/pages/login.html", {"request": request})

@router.post("/post_login", response_class=HTMLResponse)
async def post_login(
    email: str = Form(...),
    senha: str = Form(...)):
    usuario = UsuarioRepo.obter_por_email(email)
    if not usuario:
        response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Credenciais inválidas! Cheque os valores digitados a tente novamente.")
        return response
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
        adicionar_mensagem_sucesso(response, "Login realizado com sucesso!")
        return response
    else:
        response = RedirectResponse("/login", status. HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Credenciais inválidas! Cheque os valores digitados a tente novamente.")
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




@router.get("/perfil_cliente_vc", response_class=HTMLResponse)
async def get_perfil_cliente(request: Request):
    return templates.TemplateResponse("main/pages/perfil_cliente_vc.html", {"request": request})

@router.get("/perfil_prestador_vc", response_class=HTMLResponse)
async def perfil_prestador_vc(request: Request):
    return templates.TemplateResponse("main/pages/perfil_prestador_vc.html", {"request": request})

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


@router.get("/dados_cartao", response_class=HTMLResponse)
async def get_dados_cartao(request: Request):
    return templates.TemplateResponse("main/pages/dados_cartao.html", {"request": request})

@router.get("/demanda_cliente", response_class=HTMLResponse)
async def get_demanda_cliente(request: Request):
    return templates.TemplateResponse("main/pages/demanda_cliente.html", {"request": request})

@router.get("/denuncia", response_class=HTMLResponse)
async def get_denuncia(request: Request):
    return templates.TemplateResponse("main/pages/denuncia.html", {"request": request})

@router.get("/demanda_prestador", response_class=HTMLResponse)
async def get_demanda_prestador(request: Request):
    return templates.TemplateResponse("main/pages/demanda_prestador.html", {"request": request})

@router.get("/suporte_adm", response_class=HTMLResponse)
async def get_suporte_adm(request: Request):
    return templates.TemplateResponse("main/pages/suporte_adm.html", {"request": request})


@router.get("/comentario_prestador", response_class=HTMLResponse)
async def get_comentario_prestador(request: Request):
    return templates.TemplateResponse("main/pages/comentario_prestador.html", {"request": request})

@router.get("/comentario_cliente", response_class=HTMLResponse)
async def get_comentario_cliente(request: Request):
    return templates.TemplateResponse("main/pages/comentario_cliente.html", {"request": request})

@router.get("/editar_cliente", response_class=HTMLResponse)
async def get_editar_cliente(request: Request):
    return templates.TemplateResponse("main/pages/editar_cliente.html", {"request": request})

@router.get("/editar_prestador", response_class=HTMLResponse)
async def get_editar_prestador(request: Request):
    return templates.TemplateResponse("main/pages/editar_prestador.html", {"request": request})

@router.get("/encerrar_plano", response_class=HTMLResponse)
async def get_encerrar_plano(request: Request):
    return templates.TemplateResponse("main/pages/encerrar_plano.html", {"request": request})

@router.get("/perfil_cliente_vp", response_class=HTMLResponse)
async def get_perfil_cliente_vp(request: Request):
    return templates.TemplateResponse("main/pages/perfil_cliente_vp.html", {"request": request})

@router.get("/perfil_prestador_vp", response_class=HTMLResponse)
async def get_perfil_prestador_vp(request: Request):
    return templates.TemplateResponse("main/pages/perfil_prestador_vp.html", {"request": request})


@router.get("/cliente_responde", response_class=HTMLResponse)
async def get_cliente_responde(request: Request):
    return templates.TemplateResponse("main/pages/cliente_responde.html", {"request": request})


@router.get("/categorias_adm", response_class=HTMLResponse)
async def get_categorias_adm(request: Request):
    return templates.TemplateResponse("main/pages/categorias_adm.html", {"request": request})

