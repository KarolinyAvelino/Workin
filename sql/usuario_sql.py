SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        telefone TEXT NOT NULL UNIQUE,  
        categoria TEXT,
        especialidade TEXT,
        senha TEXT NOT NULL,
        perfil INT NOT NULL)
"""

SQL_INSERIR = """
    INSERT INTO usuario (nome, email, telefone, categoria, especialidade, senha, perfil)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

SQL_ALTERAR = """
    UPDATE usuario
    SET nome=?, email=?, telefone=?, categoria=?, especialidade=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM usuario    
    WHERE id=?
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, email, telefone, categoria, especialidade, perfil
    FROM usuario
    WHERE id=?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, email, telefone, categoria, especialidade, perfil
    FROM usuario
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*)
    FROM usuario
"""

SQL_EMAIL_EXISTE = """
    SELECT COUNT(*)
    FROM usuario
    WHERE email=?
"""

SQL_CHECAR_CREDENCIAIS = """
    SELECT id, nome, email, senha, perfil
    FROM usuario
    WHERE email = ?
"""

SQL_OBTER_POR_PERFIL = """
    SELECT id, nome, email, telefone, categoria, especialidade, senha, perfil
    FROM usuario
    WHERE perfil = ?
"""