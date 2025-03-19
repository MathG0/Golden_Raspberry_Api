# 🎬 API Golden Raspberry Awards

Esta API permite consultar os filmes vencedores do **Framboesa de Ouro** (Golden Raspberry Awards) e calcular os **intervalos entre vitórias dos produtores**.

## 📂 Estrutura do Projeto

/backend │── database.py → Configuração do banco de dados (SQLite) │── main.py → API desenvolvida com FastAPI │── movies.csv → Arquivo com os filmes vencedores │── test_main.py → Testes automatizados com pytest │── requirements.txt → Dependências do projeto │── README.md → Documentação do projeto

---

## 🚀 Como Rodar o Projeto

### 1️⃣ Clone o repositório
```sh
git clone https://github.com/seu-usuario/golden-raspberry-api.git
cd golden-raspberry-api
```

### 2️⃣ Crie um ambiente virtual (opcional)
```sh
python -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate     # Para Windows
```
3️⃣ Instale as dependências
```sh
pip install -r requirements.txt
```
4️⃣ Execute a API
```sh
uvicorn main:app --reload
A API será iniciada em http://127.0.0.1:8000.
```

📌 Endpoints Disponíveis

🔹 1. Página Inicial
```sh
GET /
```
Descrição: Retorna uma mensagem indicando que a API está rodando.

Resposta esperada:
json
```sh
{
  "message": "API funcionando! Vá para /docs para ver os endpoints."
}
```
🔹 2. Listar todos os filmes
```sh
GET /movies
```
Descrição: Retorna a lista de filmes carregados do movies.csv.

Resposta esperada (exemplo):
```sh
[
  {
    "id": 1,
    "title": "Jack and Jill",
    "year": 2011,
    "producer": "Adam Sandler",
    "winner": true
  },
  ...
]
```
🔹 3. Encontrar os produtores com maior/menor intervalo entre vitórias
```sh
GET /producers/intervals
```
Descrição: Retorna os produtores com o maior e o menor intervalo entre vitórias.

Resposta esperada (exemplo):
```sh
{
  "min": [
    {
      "producer": "Adam Sandler",
      "interval": 1,
      "previousWin": 2011,
      "followingWin": 2012
    }
  ],
  "max": [
    {
      "producer": "Michael De Luca",
      "interval": 7,
      "previousWin": 2008,
      "followingWin": 2015
    }
  ]
}
```
🗃️ Banco de Dados
  A API usa SQLite (database.db) para armazenar os filmes.
  
  O banco de dados é criado automaticamente ao iniciar a aplicação.
  
  Os dados são carregados do arquivo movies.csv no startup da API.

🧪 Como Rodar os Testes
Instale as dependências de testes:

```sh
pip install pytest
```
Execute os testes automatizados:
```sh
pytest test_main.py
```
Se todos os testes passarem, a saída será semelhante a:
```sh
========================== 2 passed in 0.72s ==========================
```
🔗 Acesse a Documentação Interativa

Após rodar a API, acesse o Swagger UI para testar os endpoints:
```sh
📌 http://127.0.0.1:8000/docs (Swagger UI)
📌 http://127.0.0.1:8000/redoc (ReDoc)
👨‍💻 Tecnologias Utilizadas
✅ FastAPI - Framework para criação de APIs rápidas e eficientes
✅ SQLAlchemy - ORM para interação com banco de dados SQLite
✅ Pydantic - Validação de dados
✅ pytest - Framework de testes
```
