import dotenv
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from routes.main_routes import router as main_routes
from repositories.usuario_repo import UsuarioRepo
from routes import main_routes, rotas_cliente
from util.auth import checar_permissao, checar_autenticacao
from util.exceptions import configurar_excecoes

from routes.main_routes import router as main_router
from routes.rotas_admin import router as admin_router
from routes.rotas_cliente import router as cliente_router
from routes.rotas_prestador import router as prestador_router

UsuarioRepo.criar_tabela()  #criação da tabela

app = FastAPI() #criação do objeto
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.middleware(middleware_type="http")(checar_autenticacao)  #erro
configurar_excecoes(app)
app.include_router(main_routes.router)  #incluir arquivos de rota

dotenv.load_dotenv()
UsuarioRepo.criar_tabela()
app = FastAPI(dependencies=[Depends(checar_permissao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware("http")(checar_autenticacao)
configurar_excecoes(app)

app.include_router(main_router)
app.include_router(admin_router)
app.include_router(cliente_router)
app.include_router(prestador_router)





# load_dotenv()
# UsuarioRepo.criar_tabela()
# app = FastAPI(dependencies=[Depends(checar_autorizacao)])
# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.middleware("http")(checar_autenticacao)
# tratar_excecoes(app)

# app.include_router(public_router)
# app.include_router(usuario_router)
# app.include_router(aluno_router)
# app.include_router(professor_router)
