## Projeto Dash
Extração de dados de pdf's criação de gráficos.

#### Execução do Projeto

1- Com docker:
```sh
docker-compose build
docker-compose up
```
rodar fora do docker:

```sh
poetry config virtualenvs.in-project true
poetry install
python src/main.py
```

Acessar serviço: `http://localhost:8080`.

É criado um usuário default `admin` e password `admin123`.
