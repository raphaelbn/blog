# Blog Api

Projeto utilizando Django Rest Framework que simula um Blog.

Nesse projeto podemos gerir cadastros de usuários. Cada usuário autenticado poderá criar, deletar, atualizar e listar Posts, dentro da API.

Autenticação customizada via JWT.

Testes de API utilizando APITestCase do DRF.


### Instruções para uso via Docker:

```
docker-compose up -d --build
```

```
docker-compose exec app python manage.py migrate
```

A aplicação ficará disponível localmente na porta 8000.