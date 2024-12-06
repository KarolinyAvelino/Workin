import json
import sqlite3
from typing import Optional
from models.usuario_model import Usuario
from sql.usuario_sql import *
from util.auth import conferir_senha
from util.database import obter_conexao


class UsuarioRepo:
    @classmethod
    def criar_tabela(cls):
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_CRIAR_TABELA)
                conexao.commit()
        except sqlite3.Error as ex:
            print(f"Erro ao criar tabela: {ex}")

    @classmethod
    def inserir(cls, usuario: Usuario) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        usuario.nome,
                        usuario.email,
                        usuario.telefone,
                        usuario.categoria,
                        usuario.especialidade,
                        usuario.senha,
                        usuario.perfil,
                    ),
                )
                conexao.commit()  # Importante para confirmar a transação
                if cursor.rowcount > 0:
                    return usuario
                else:
                    print("Nenhum registro foi inserido.")
        except sqlite3.Error as ex:
            print(f"Erro ao inserir usuário: {ex}")
            
            
        return None
    @classmethod
    def alterar(cls, usuario: Usuario) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (                        
                        usuario.nome,
                        usuario.email,
                        usuario.telefone,
                        usuario.categoria,
                        usuario.especialidade,
                        usuario.perfil,
                        usuario.id,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Usuario]:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor = conexao.cursor()
            dados = cursor.execute(
                SQL_OBTER_POR_ID, (id,)).fetchone()
            if dados:
                return Usuario(*dados)
            return None
        
    @classmethod
    def obter_por_email(cls, email: str) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_EMAIL, (email,)).fetchone()
                if tupla:
                    usuario = Usuario(*tupla)
                    return usuario
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def obter_quantidade(cls) -> int:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return 0

    @classmethod
    def inserir_dados_json(cls):
        if UsuarioRepo.obter_quantidade() == 0:
            with open("sql/usuarios.json", "r", encoding="utf-8") as arquivo:
                usuarios = json.load(arquivo)
                for usuario in usuarios:
                    UsuarioRepo.inserir(Usuario(**usuario))

    @classmethod
    def email_existe(cls, email: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_EMAIL_EXISTE, (email,)).fetchone()
                return tupla[0] > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def checar_credenciais(cls, email: str, senha: str) -> Optional[tuple]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(
                SQL_CHECAR_CREDENCIAIS, (email,)).fetchone()
            if dados:
                if conferir_senha(senha, dados[3]):
                    return (dados[0], dados[1], dados[2], dados[4])
            return None

    @staticmethod
    def obter_por_perfil(perfil: int) -> list[Usuario]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_POR_PERFIL, (perfil,))
            dados = cursor.fetchall()
            if dados is None:
                return []
            return [Usuario(**usuario) for usuario in dados]