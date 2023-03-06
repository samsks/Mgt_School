# README

## Índice

- [README](#readme)
  - [Índice](#índice)
  - [Introdução](#introdução)
  - [Pré-requisitos](#pré-requisitos)
  - [Instruções](#instruções)
  - [Documentação](#documentação)
  - [Licença](#licença)

## Introdução

Este é um guia simples para executar um projeto em Python, que usa um ambiente virtual, gerenciador de pacotes pip e um banco de dados que precisa de migrações.

## Pré-requisitos

Para seguir este guia, você precisará ter o Python instalado em sua máquina. Você pode baixar o Python no site oficial [python.org](https://www.python.org/downloads/).

## Instruções

1. Crie seu ambiente virtual usando o seguinte comando no terminal:
   Obs: Este repositório é compartilhado. Verifique se está na pasta django-app.

```
python -m venv venv
```

O comando acima criará um ambiente virtual chamado "venv".

1. Ative o ambiente virtual com um dos seguintes comandos, dependendo do seu sistema operacional:

- **Linux**

  ```
  source venv/bin/activate
  ```

- **Windows**

  ```
  .\venv\Scripts\activate
  ```

Quando o ambiente virtual estiver ativo, você deve ver `(venv)` no início de sua linha de comando.

3. Instale as dependências do projeto usando o seguinte comando no terminal:

```
pip install -r requirements.txt
```

Este comando instalará todas as dependências listadas no arquivo `requirements.txt`.

4. Execute as migrações do banco de dados com o seguinte comando no terminal:

```
python manage.py migrate
```

Este comando executará as migrações necessárias para configurar o banco de dados do projeto.

5. Agora você está pronto para executar o projeto! Use o seguinte comando para iniciar o servidor:

```
python manage.py runserver
```

Este comando iniciará o servidor da aplicação. Acesse a aplicação no navegador da web, digitando `http://127.0.0.1:8000/` na barra de endereço.

6. Quando terminar de usar o projeto, você pode desativar o ambiente virtual com o seguinte comando no terminal:

```
deactivate
```

Este comando desativará o ambiente virtual e retornará ao ambiente global do Python.

## Documentação

1. Acesse a documentação da API:

- Acesse `http://localhost:8000/api/docs/swagger-ui/` para visualizar a documentação com estilo SWAGGER.
- Acesse `http://localhost:8000/api/docs/redoc/` para visualizar a documentação com estilo REDOC.

## Link de Produção

1. Acesse a API online (Se disponível):
- Acesse `https://web-production-1b55.up.railway.app/admin/` para acessar com superuser.
- Acesse `https://web-production-1b55.up.railway.app/api/account/` para acessar as requisições. Trocar o endpoint conformedocumentação para acessar as rotas.
- Acesse `https://web-production-1b55.up.railway.app/api/docs/swagger-ui/` para visualizar a documentação com estilo SWAGGER.
- Acesse `https://web-production-1b55.up.railway.app0/api/docs/redoc/` para visualizar a documentação com estilo REDOC.

## Licença

Este projeto está licenciado sob a Licença All Rights Reserved - veja o arquivo [LICENSE](../LICENSE.md) para mais detalhes.
