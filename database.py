# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Cria o engine de conexão com o banco de dados MySQL
# 'create_engine' estabelece a comunicação com o banco de dados utilizando a URL acima.
engine = create_engine(DATABASE_URL)

# 'sessionmaker' cria sessões que serão usadas para realizar transações no banco de dados.
# 'autocommit=False' desativa o autocommit, ou seja, precisamos explicitamente fazer o commit.
# 'autoflush=False' impede o envio automático das mudanças para o banco até que chamemos 'commit()'.
# Quando passamos bind=engine, estamos dizendo que todas as sessões criadas por SessionLocal (a fábrica de sessões) estarão conectadas ao banco de dados que o engine está configurado para se comunicar.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 'Base' serve como uma classe base para todos os modelos que definirmos. Ela contém metadados necessários para criar as tabelas.
Base = declarative_base()

# Função que cria uma dependência para a sessão do banco de dados.
# 'get_db' fornece uma sessão para ser usada nas operações de banco de dados.
# 'yield' permite a utilização de uma sessão temporária para a transação e, depois de usada, ela será fechada com 'db.close()'.
# No contexto de FastAPI, o yield é utilizado para gerenciar recursos, como sessões de banco de dados, conexões com APIs externas, ou arquivos que precisam ser abertos e fechados. 
# # Quando usamos yield em uma função de dependência como get_db(), estamos criando um mecanismo que abre um recurso (neste caso, uma sessão de banco de dados), retorna esse recurso temporariamente para ser usado na rota e, em seguida, limpa ou fecha o recurso quando ele não for mais necessário.
def get_db():
    db = SessionLocal()
    try:
        yield db  # Entrega a sessão para uso nas rotas da API
    finally:
        db.close()  # Fecha a sessão após a conclusão da transação
