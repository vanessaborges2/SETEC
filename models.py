# models.py

from sqlalchemy import Column, Integer, String  
# Importa as classes necessárias da SQLAlchemy para definir colunas e tipos de dados nas tabelas
from database import Base  
# Importa a classe Base, que é a classe base declarativa de SQLAlchemy para definir o modelo de banco de dados
from pydantic import BaseModel, EmailStr  
# Importa o BaseModel e EmailStr de Pydantic, que serão usados para validação de dados na API

# Modelo de tabela no banco de dados
class AlunoDB(Base):  # Define o modelo da tabela "alunos" que será mapeado para o banco de dados
    __tablename__ = "alunos"  # Especifica o nome da tabela no banco de dados como "alunos"

    id = Column(Integer, primary_key=True, index=True)  # Cria a coluna 'id' como chave primária (primary_key=True) e com índice (index=True)
    nome = Column(String(100), nullable=False)  # Cria a coluna 'nome' do tipo String com até 100 caracteres e define que ela não pode ser nula (nullable=False)
    email = Column(String(100), nullable=False)  # Cria a coluna 'email' do tipo String com até 100 caracteres, também não pode ser nula
    ra = Column(String(50), unique=True, nullable=False)  # Cria a coluna 'ra' (registro acadêmico), que deve ser única (unique=True) e não nula

# Modelo Pydantic para criação de alunos
class Aluno(BaseModel):  # Define o modelo Pydantic, que será utilizado para validação e serialização de dados
    nome: str  # O campo 'nome' deve ser uma string
    email: EmailStr  # O campo 'email' deve ser um e-mail válido, validado pelo tipo específico EmailStr do Pydantic
    ra: str  # O campo 'ra' deve ser uma string

    class Config:  # Define uma configuração especial para o modelo
        orm_mode = True  # 'orm_mode' habilita o Pydantic para trabalhar diretamente com objetos do SQLAlchemy, convertendo-os em dados Pydantic

