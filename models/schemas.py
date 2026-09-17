#arquivo para estruturação de arquivos com pydantic, onde vamos formatar o JSON

from typing import Optional

from pydantic import BaseModel, Field


class Prova(BaseModel):
    data: Optional[str] = None
    materia: Optional[str] = None


class Duvida(BaseModel):
    aluno: Optional[str] = None
    descricao: str


class Advertencia(BaseModel):
    aluno: Optional[str] = None
    motivo: str


class Aula(BaseModel):
    materia: Optional[str] = None
    assunto: Optional[str] = None
    provas: list[Prova] = Field(default_factory=list)
    duvidas: list[Duvida] = Field(default_factory=list)
    advertencias: list[Advertencia] = Field(default_factory=list)
