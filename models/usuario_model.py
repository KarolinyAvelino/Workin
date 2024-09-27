from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    categoria: Optional[str] = None
    especialidade: Optional[str] = None
    senha: Optional[str] = None
    perfil: Optional[int] = None

