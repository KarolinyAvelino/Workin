from fastapi import Depends, FastAPI # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from repositories.usuario_repo import UsuarioRepo
from routes import main_routes
from util.auth import checar_permissao, middleware_autenticacao
from util.exceptions import configurar_excecoes

UsuarioRepo.criar_tabela()  #criação da tabela
app = FastAPI(dependencies=[Depends(checar_permissao)]) #criação do objeto
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware(middleware_type="http")(middleware_autenticacao)  #erro
configurar_excecoes(app)
app.include_router(main_routes.router)  #incluir arquivos de rota