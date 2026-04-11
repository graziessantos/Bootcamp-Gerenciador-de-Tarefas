# Gerenciador de Tarefas Pessoais

## Descrição do Problema Real

A dificuldade de organizar e priorizar tarefas do dia a dia é um problema comum que afeta estudantes, trabalhadores e qualquer pessoa que precise equilibrar múltiplas responsabilidades. Sem uma ferramenta adequada, é fácil esquecer compromissos, misturar prioridades e perder prazos importantes — o que gera estresse, queda de produtividade e sensação de sobrecarga.

Este projeto propõe uma solução simples e direta: um gerenciador de tarefas acessível via navegador, que permite cadastrar, organizar e acompanhar tarefas com prioridade e categoria definidas pelo próprio usuário.

---

## Público-Alvo

- Estudantes que precisam organizar atividades de estudo, escola ou faculdade
- Profissionais que gerenciam demandas de trabalho e projetos
- Qualquer pessoa que queira manter uma lista de tarefas pessoais com controle de prioridade

---

## Funcionalidades Principais

- Cadastrar tarefas com título, descrição, data de prazo e situação (pendente/concluída)
- Definir prioridade visual: 🔴 Urgente, 🟡 Pode Esperar, 🟢 Sem Urgência
- Informar a categoria livremente (ex: Estudo, Trabalho, Faculdade, Escola, Pessoal, Saúde) com sugestões automáticas
- Listar todas as tarefas em uma tabela com filtro por prioridade
- Editar e excluir tarefas existentes
- Visualizar resumo de tarefas por prioridade e total de pendências

---

## Tecnologias Utilizadas

- **Python 3.11+**
- **Django 4.2** — framework web
- **SQLite** — banco de dados local (padrão do Django)
- **Bootstrap 5.3** — interface responsiva
- **pytest + pytest-django** — testes automatizados
- **ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)

---

## Instruções de Instalação

**Pré-requisitos:** Python 3.11 ou superior instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# 2. Crie e ative um ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações do banco de dados
python manage.py migrate
```

---

## Instruções de Execução

```bash
# Inicie o servidor de desenvolvimento
python manage.py runserver
```

Acesse no navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Como Rodar os Testes

```bash
pytest tests/
```

Os testes cobrem: criação de tarefa, representação em string, listagem, valor padrão do campo `concluida`, categoria livre e remoção de tarefa.

---

## Como Rodar o Lint

```bash
ruff check .
```

Para corrigir automaticamente os problemas identificados:

```bash
ruff check . --fix
```

---

## Versão Atual

`2.1.1`

---

## Autor
Grazielle Santana dos Santos
 
[Link do Repositório no GitHub] 
https://github.com/graziessantos/Bootcamp-Gerenciador-de-Tarefas