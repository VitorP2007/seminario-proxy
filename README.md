# Projeto: Demonstração de Proxy Reverso com NGINX

Projeto acadêmico que demonstra, de forma prática, o funcionamento de um **Proxy Reverso** utilizando **NGINX**, **Python com Flask** e **Docker Compose**. A aplicação também utiliza o recurso **Rate Limiting** do NGINX para limitar a quantidade de requisições recebidas.

## 1. Objetivo

O objetivo do projeto é apresentar como um Proxy Reverso recebe as requisições dos usuários, encaminha essas solicitações para um servidor de aplicação e devolve as respostas ao cliente.

Na demonstração, o NGINX atua como Proxy Reverso e encaminha as requisições para uma aplicação backend desenvolvida com Flask. Os dois serviços são executados em contêineres separados e se comunicam por meio da rede criada pelo Docker Compose.

## 2. Tecnologias utilizadas

- **NGINX:** recebe as requisições HTTP e as encaminha para o backend.
- **Python:** linguagem utilizada no desenvolvimento do backend.
- **Flask:** framework responsável pela aplicação backend e pelas rotas de teste.
- **Docker:** executa os serviços em contêineres separados.
- **Docker Compose:** organiza e executa os serviços do projeto em conjunto.

## 3. Como funciona

O fluxo de uma requisição acontece da seguinte maneira:

1. O usuário acessa a aplicação pelo navegador ou por uma ferramenta como o `curl`.
2. A requisição chega ao NGINX, publicado na porta `8080` do computador.
3. O NGINX encaminha a requisição para o serviço `backend`, na porta `8000`, pela rede interna do Docker.
4. O Flask processa a solicitação e envia uma resposta ao NGINX.
5. O NGINX devolve a resposta ao usuário.

**Observação:** a porta `8000` do backend não é publicada diretamente no computador. Por isso, o acesso externo à aplicação é feito pelo NGINX, na porta `8080`.

## 4. Estrutura do projeto

```text
proxy-reverso/
├── backend/
│   ├── .venv/              # Ambiente virtual local (não necessário para executar com Docker)
│   ├── app.py              # Aplicação Flask e suas rotas
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile          # Instruções para criar a imagem do backend
├── nginx/
│   └── default.conf        # Configuração do NGINX e do Proxy Reverso
└── docker-compose.yml      # Configuração dos serviços e da comunicação entre eles
```

## 5. Requisitos

Para executar o projeto, é necessário ter instalado:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows, macOS ou Linux compatível).
- Docker Compose, disponibilizado pelo comando `docker compose` nas versões atuais do Docker Desktop.

No Windows, os comandos abaixo podem ser executados no PowerShell. Antes de iniciar, abra o Docker Desktop e aguarde até que o Docker esteja funcionando.

## 6. Como executar o projeto

### 6.1. Obter os arquivos

Clone o repositório ou baixe os arquivos do projeto. Depois, abra o terminal na pasta principal `proxy-reverso`, onde está localizado o arquivo `docker-compose.yml`.

Exemplo de clonagem:

```bash
git clone https://github.com/VitorP2007/seminario-proxy.git
cd proxy-reverso
```

### 6.2. Construir e iniciar os contêineres

Execute:

```bash
docker compose up --build -d
```

Esse comando constrói a imagem do backend, cria os contêineres necessários e inicia os serviços em segundo plano.

### 6.3. Verificar os serviços

Para conferir se os contêineres estão em execução:

```bash
docker compose ps
```

Devem aparecer os serviços `nginx` e `backend` em execução.

### 6.4. Acessar a aplicação

Abra o navegador no endereço:

```text
http://localhost:8080/
```

Também é possível testar pelo terminal:

```bash
curl.exe -i http://127.0.0.1:8080/
```

A resposta esperada é `HTTP/1.1 200 OK`, acompanhada dos dados retornados pelo Flask.

A segunda rota disponível é:

```text
http://localhost:8080/sobre
```

Ou, pelo terminal:

```bash
curl.exe -i http://127.0.0.1:8080/sobre
```

## 7. Testar o acesso ao backend

O backend utiliza a porta `8000` dentro da rede do Docker, mas essa porta não está publicada diretamente no computador.

No PowerShell, execute:

```powershell
curl.exe -i http://127.0.0.1:8000/
```

A tentativa de conexão direta deve falhar, pois não existe publicação dessa porta no host.

Agora teste pelo NGINX:

```powershell
curl.exe -i http://127.0.0.1:8080/
```

Nesse caso, a aplicação deve responder normalmente. Isso demonstra que o acesso externo está sendo feito pelo Proxy Reverso.

## 8. Rate Limiting

O projeto possui uma configuração de **Rate Limiting** no NGINX. Esse recurso controla a frequência de requisições recebidas.

A configuração utilizada estabelece um limite de **1 requisição por segundo** para cada endereço IP identificado pelo NGINX. Quando uma requisição ultrapassa o limite, ela pode ser rejeitada com o código HTTP `429 — Too Many Requests`.

Trecho principal da configuração em `nginx/default.conf`:

```nginx
limit_req_zone $binary_remote_addr
    zone=meulimite:10m
    rate=1r/s;

server {
    listen 80;
    server_name _;
    limit_req_status 429;

    location / {
        limit_req zone=meulimite;
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Como testar

Acesse a aplicação normalmente:

```powershell
curl.exe -i http://127.0.0.1:8080/
```

A resposta pode ser `200 OK` quando a requisição é aceita.

Para observar o limite, faça duas requisições rapidamente, uma logo após a outra, usando o mesmo endereço:

```powershell
curl.exe -i http://127.0.0.1:8080/; curl.exe -i http://127.0.0.1:8080/
```

No PowerShell, o ponto e vírgula separa os dois comandos. Como o limite é de uma requisição por segundo e não foi configurado `burst`, uma das respostas poderá ser `429 Too Many Requests` se as solicitações chegarem dentro do mesmo intervalo de limitação. O resultado depende do intervalo real entre as requisições.

Aguarde alguns segundos entre os testes para que o limite seja renovado.

## 9. Comandos úteis

| Comando | Finalidade |
|---|---|
| `docker compose up --build -d` | Constrói e inicia os serviços em segundo plano. |
| `docker compose ps` | Mostra o estado dos contêineres. |
| `docker compose logs --tail=30 nginx` | Exibe as últimas linhas do log do NGINX. |
| `docker compose logs --tail=30 backend` | Exibe as últimas linhas do log do backend. |
| `docker compose exec nginx nginx -t` | Verifica a sintaxe da configuração do NGINX. |
| `docker compose exec nginx nginx -s reload` | Recarrega a configuração do NGINX. |
| `docker compose down` | Para e remove os contêineres e a rede criados pelo Compose. |

Depois de alterar `nginx/default.conf`, valide e recarregue a configuração:

```bash
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
```

Se a alteração também envolver a construção da imagem do backend, execute novamente:

```bash
docker compose up --build -d
```

## 10. Solução de problemas

**A página não abre em `localhost:8080`:**

- Verifique se o Docker Desktop está em execução.
- Execute `docker compose ps` para conferir se os serviços estão ativos.
- Consulte os logs com `docker compose logs --tail=30 nginx` e `docker compose logs --tail=30 backend`.

**O NGINX apresenta erro na configuração:**

- Execute `docker compose exec nginx nginx -t`.
- Confira o arquivo `nginx/default.conf` e corrija eventuais erros indicados pelo comando.

**Aparece HTTP 429 durante os testes:**

- Isso pode ser causado pelo Rate Limiting.
- Aguarde alguns segundos e tente novamente.

**O backend não inicia:**

- Confira o `backend/Dockerfile`, o `backend/requirements.txt` e os logs do serviço com `docker compose logs --tail=30 backend`.

## 11. Limitações da demonstração

Este projeto foi desenvolvido para fins acadêmicos e demonstração local do funcionamento de um Proxy Reverso. A configuração apresentada não representa, por si só, uma implantação pronta para produção. Recursos adicionais, como HTTPS com certificado TLS, autenticação, monitoramento e ajustes de segurança para um ambiente real, exigiriam configuração e testes próprios.

## 12. Integrantes

- Érick Sanchez de Jesus Afonso
- Milena Pires Mendes
- Vitor Pizolato da Silva

**Disciplina:** Web I 
**Instituição:** IF Baiano / Campus Guanambi  
**Ano:** 2026