import dotenv
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.usuario_repo import UsuarioRepo
from util.auth import checar_permissao, checar_autenticacao
from util.exceptions import configurar_excecoes
from routes import main_routes, rotas_admin, rotas_cliente, rotas_prestador

UsuarioRepo.criar_tabela()  #criação da tabela

dotenv.load_dotenv()
UsuarioRepo.criar_tabela()
app = FastAPI(dependencies=[Depends(checar_permissao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware("http")(checar_autenticacao)
configurar_excecoes(app)

app.include_router(main_routes.router)  #incluir arquivos de rota
app.include_router(rotas_admin.router)
app.include_router(rotas_prestador.router)
app.include_router(rotas_cliente.router)


# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from routes.main_routes import router as main_routes
# from repositories.usuario_repo import UsuarioRepo
# from routes import main_routes, rotas_admin, rotas_cliente, rotas_prestador
# from util.auth import checar_permissao, checar_autenticacao
# from util.exceptions import configurar_excecoes

# UsuarioRepo.criar_tabela()  #criação da tabela

# app = FastAPI() #criação do objeto
# app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

# app.middleware(middleware_type="http")(checar_autenticacao)  #erro
# configurar_excecoes(app)
# app.include_router(main_routes.router)  #incluir arquivos de rota
# app.include_router(rotas_admin.router)
# app.include_router(rotas_prestador.router)
# app.include_router(rotas_cliente.router)







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
