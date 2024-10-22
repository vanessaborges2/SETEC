# main.py

from fastapi import FastAPI
# Importa a classe 'FastAPI', que é usada para criar a aplicação web FastAPI.

from models import AlunoDB
# Importa o modelo 'AlunoDB' definido no arquivo 'models.py'. Esse modelo representa a tabela de alunos no banco de dados.

from database import engine
# Importa o 'engine', que é o objeto de conexão com o banco de dados, criado em 'database.py'.
# O 'engine' é responsável por gerenciar as interações com o banco de dados MySQL.

from alunos import router as alunos_router  # Importa o roteador de alunos
# Importa o roteador de rotas do arquivo 'alunos.py', renomeando-o para 'alunos_router'. 
# Esse roteador contém todas as rotas relacionadas ao CRUD de alunos, como criar, listar, buscar, atualizar e deletar.

# Criar as tabelas no banco de dados
AlunoDB.metadata.create_all(bind=engine)
# Gera as tabelas no banco de dados com base nos modelos definidos, neste caso, o 'AlunoDB'.
# 'metadata.create_all(bind=engine)' garante que, se as tabelas ainda não existirem no banco de dados, elas serão criadas.
# O 'engine' está associado ao banco de dados, garantindo que as tabelas sejam criadas no banco configurado.

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Cria uma instância da aplicação FastAPI, que é usada para definir as rotas, middlewares e configurações gerais da API.

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (pode ser restrito a domínios específicos)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Incluir as rotas do arquivo alunos.py
app.include_router(alunos_router)
# Adiciona as rotas definidas em 'alunos.py' ao aplicativo FastAPI principal. 
# Todas as rotas dentro de 'alunos_router' (como /alunos/) serão agora acessíveis através da aplicação FastAPI.

@app.on_event("startup")
# Define um evento de inicialização ('startup') que é executado quando o servidor FastAPI é iniciado.
# Funções decoradas com '@app.on_event("startup")' são executadas automaticamente antes de a API começar a aceitar requisições.

async def startup():
    AlunoDB.metadata.create_all(bind=engine)
    # Durante o evento de inicialização, este comando verifica e garante que todas as tabelas relacionadas ao modelo 'AlunoDB' estejam criadas no banco de dados.
    # Isso é especialmente útil para garantir que o banco de dados esteja pronto para uso quando a API começar a aceitar requisições.
