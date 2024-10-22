# alunos.py

from fastapi import APIRouter, Depends, HTTPException
# Importa as funções e classes do FastAPI:
# - APIRouter: Usado para criar um roteador que agrupa as rotas relacionadas.
# - Depends: Usado para injetar dependências, como a sessão de banco de dados nas rotas.
# - HTTPException: Usado para lançar exceções HTTP personalizadas, como erros 404 ou 400.

from sqlalchemy.orm import Session
# Importa a classe 'Session' da SQLAlchemy, que representa uma sessão de banco de dados. 
# Ela será usada para interagir com o banco dentro das rotas.

from models import AlunoDB, Aluno
# Importa os modelos definidos no arquivo 'models.py':
# - AlunoDB: O modelo SQLAlchemy que representa a tabela de alunos no banco de dados.
# - Aluno: O modelo Pydantic que é usado para validar os dados de entrada e saída da API.

from database import get_db
# Importa a função 'get_db' do arquivo 'database.py', que é usada para criar uma sessão de banco de dados.

from sqlalchemy.exc import IntegrityError
# Importa a exceção 'IntegrityError' do SQLAlchemy, que será usada para capturar erros de integridade, como a tentativa de inserir um RA duplicado.

# Cria um roteador para as rotas de alunos
router = APIRouter()
# Instancia um APIRouter, que agrupa e gerencia as rotas da API relacionadas ao contexto de alunos.
# Esse roteador será incluído no app principal em 'main.py'.

@router.post("/alunos/", response_model=Aluno)
# Define a rota POST "/alunos/" para criar um novo aluno. O parâmetro 'response_model=Aluno' indica que a resposta da rota será validada e formatada conforme o modelo Pydantic 'Aluno'.
async def criar_aluno(aluno: Aluno, db: Session = Depends(get_db)):
    # Função assíncrona que cria um novo aluno no banco de dados.
    # Recebe:
    # - 'aluno': Um objeto do tipo 'Aluno' validado via Pydantic.
    # - 'db': Uma sessão de banco de dados, obtida através de dependência injetada com 'get_db()'.
    
    aluno_db = AlunoDB(nome=aluno.nome, email=aluno.email, ra=aluno.ra)
    # Cria uma nova instância do modelo SQLAlchemy 'AlunoDB' com os dados do aluno passado via 'aluno'.

    try:
        db.add(aluno_db)
        # Adiciona o novo aluno à sessão de banco de dados, mas ainda não o grava no banco de dados.

        db.commit()
        # Confirma as mudanças e grava o novo aluno no banco de dados.

        db.refresh(aluno_db)
        # Atualiza o objeto 'aluno_db' com os dados mais recentes do banco, como o 'id' gerado automaticamente.

        return aluno_db
        # Retorna o objeto 'aluno_db', agora gravado no banco de dados, como resposta da API.

    except IntegrityError:
        # Captura erros de integridade, como a tentativa de inserir um RA duplicado.

        db.rollback()
        # Desfaz qualquer transação pendente para evitar a corrupção dos dados no banco.

        raise HTTPException(status_code=400, detail="Aluno com esse RA já existe.")
        # Lança uma exceção HTTP 400 informando que o RA do aluno já existe.

@router.get("/alunos/", response_model=list[Aluno])
# Define a rota GET "/alunos/" para listar todos os alunos.
# O parâmetro 'response_model=list[Aluno]' indica que a resposta será uma lista de objetos validados pelo modelo 'Aluno'.
async def listar_alunos(db: Session = Depends(get_db)):
    # Função assíncrona que lista todos os alunos do banco de dados.
    # Recebe uma sessão de banco de dados como dependência injetada.

    return db.query(AlunoDB).all()
    # Realiza uma consulta no banco de dados buscando todos os registros da tabela 'AlunoDB'.
    # Retorna a lista de alunos.

@router.get("/alunos/{ra}", response_model=Aluno)
# Define a rota GET "/alunos/{ra}" para obter um aluno específico baseado no RA.
# O parâmetro 'response_model=Aluno' valida a resposta da API para que esteja de acordo com o modelo 'Aluno'.
async def obter_aluno(ra: str, db: Session = Depends(get_db)):
    # Função assíncrona que obtém um aluno específico pelo RA.
    # Recebe:
    # - 'ra': O RA do aluno passado como parâmetro na URL.
    # - 'db': A sessão de banco de dados, injetada como dependência.

    aluno = db.query(AlunoDB).filter(AlunoDB.ra == ra).first()
    # Realiza uma consulta no banco de dados buscando o aluno com o RA fornecido.
    # 'filter' aplica o filtro pelo RA, e 'first()' retorna o primeiro registro correspondente.

    if aluno is None:
        # Verifica se o aluno foi encontrado.
        
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
        # Se o aluno não for encontrado, lança uma exceção HTTP 404 com a mensagem "Aluno não encontrado".

    return aluno
    # Retorna o aluno encontrado.

@router.put("/alunos/{ra}", response_model=Aluno)
# Define a rota PUT "/alunos/{ra}" para atualizar um aluno específico com base no RA.
# O parâmetro 'response_model=Aluno' valida e formata a resposta da API conforme o modelo 'Aluno'.
async def atualizar_aluno(ra: str, aluno_atualizado: Aluno, db: Session = Depends(get_db)):
    # Função assíncrona que atualiza os dados de um aluno.
    # Recebe:
    # - 'ra': O RA do aluno a ser atualizado, passado como parâmetro na URL.
    # - 'aluno_atualizado': O objeto Pydantic contendo os novos dados do aluno.
    # - 'db': A sessão de banco de dados, injetada como dependência.

    aluno = db.query(AlunoDB).filter(AlunoDB.ra == ra).first()
    # Busca o aluno no banco de dados pelo RA.

    if aluno is None:
        # Verifica se o aluno foi encontrado.

        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
        # Se o aluno não for encontrado, lança uma exceção HTTP 404.

    aluno.nome = aluno_atualizado.nome
    aluno.email = aluno_atualizado.email
    # Atualiza os campos 'nome' e 'email' do aluno com os novos dados recebidos.

    db.commit()
    # Confirma as mudanças no banco de dados.

    db.refresh(aluno)
    # Atualiza o objeto 'aluno' com os dados mais recentes do banco.

    return aluno
    # Retorna o aluno atualizado como resposta.

@router.delete("/alunos/{ra}", response_model=Aluno)
# Define a rota DELETE "/alunos/{ra}" para deletar um aluno específico com base no RA.
# O parâmetro 'response_model=Aluno' valida e formata a resposta da API conforme o modelo 'Aluno'.
async def deletar_aluno(ra: str, db: Session = Depends(get_db)):
    # Função assíncrona que deleta um aluno específico pelo RA.
    # Recebe:
    # - 'ra': O RA do aluno a ser deletado.
    # - 'db': A sessão de banco de dados, injetada como dependência.

    aluno = db.query(AlunoDB).filter(AlunoDB.ra == ra).first()
    # Busca o aluno no banco de dados pelo RA.

    if aluno is None:
        # Verifica se o aluno foi encontrado.

        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
        # Se o aluno não for encontrado, lança uma exceção HTTP 404.

    db.delete(aluno)
    # Deleta o aluno encontrado no banco de dados.

    db.commit()
    # Confirma a exclusão do aluno no banco de dados.

    return aluno
    # Retorna o aluno deletado como resposta (antes de sua exclusão).
