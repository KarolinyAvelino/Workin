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
            "link": "/perfil_prestador"  
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

    return templates.TemplateResponse("prestador/pages/planos.html", {"request": request, "planos": planos})


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