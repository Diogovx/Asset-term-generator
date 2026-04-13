# Gerador de Termos de Ativos e Passivos Snipe-IT

[Leia em Inglês](./README.md)

[![Qualidade e Teste de CI](https://github.com/Diogovx/Asset-term-generator/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/Diogovx/Asset-term-generator/actions/workflows/ci-pipeline.yml)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Estilo de código: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Verificado com mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Uma aplicação de linha de comando (CLI) Python que automatiza a criação de documentos de termos de responsabilidade para ativos de TI atribuídos a funcionários, consultando dados diretamente de uma instância do Snipe-IT.

## 📋 Índice

- [Gerador de Termos de Ativos e Passivos Snipe-IT](#gerador-de-termos-de-ativos-e-passivos-snipe-it)
  - [📋 Índice](#-índice)
  - [✨ Recursos](#-recursos)
  - [🚀 Instalação e Configuração](#-instalação-e-configuração)
  - [🛠️ Uso](#️-uso)
  - [✅ Testes](#-testes)
  - [🔧 Personalização de Templates (Jinja2)](#-personalização-de-templates-jinja2)
    - [As 3 Regras de Ouro das Tags Jinja2](#as-3-regras-de-ouro-das-tags-jinja2)
    - [Dados Disponíveis em Modelos (Contexto)](#dados-disponíveis-em-modelos-contexto)
      - [Objeto `user`](#objeto-user)
      - [Objeto `asset`](#objeto-asset)
    - [Exemplos Práticos](#exemplos-práticos)
      - [1. Exibindo um Parágrafo Condicionalmente](#1-exibindo-um-parágrafo-condicionalmente)
      - [2. Listando Todos os Acessórios](#2-listando-todos-os-acessórios)
  - [🏛️ Decisões de Arquitetura e Design](#️-decisões-de-arquitetura-e-design)
  - [📈 Roteiro](#-roteiro)
  - [🤝 Contribuindo](#-contribuindo)
  - [✍️ Autores](#️-autores)
  - [📄 Licença](#-licença)

---

## ✨ Recursos

- **Busca Inteligente:** Encontra usuários pelo número de funcionário e busca todos os seus ativos associados (hardware, componentes e acessórios).
- **Geração Dinâmica Poderosa:** Utiliza modelos `.docx` desenvolvidos pelo **mecanismo de templates Jinja2**, permitindo lógica complexa como condicionais (`if/else`) e loops (`for`) diretamente no documento do Word.
- **Arquitetura Robusta:** Construída com Pydantic para validação de dados, garantindo a integridade das informações da API.
- **Qualidade Garantida:** Pipeline de CI/CD com GitHub Actions para executar testes (`pytest`) e análises de código (`ruff`, `mypy`) automaticamente.
- **Ambiente Reproduzível:** Gerenciamento de dependências com `pip-tools` para garantir um ambiente de desenvolvimento consistente por meio de arquivos de bloqueio.

---

## 🚀 Instalação e Configuração

Siga estes passos para configurar o ambiente de desenvolvimento em sua máquina.

1. **Clone o repositório:**

    ```bash
    git clone [https://github.com/Diogovx/Asset-term-generator.git](https://github.com/Diogovx/Asset-term-generator.git)
    cd Asset-term-generator
    ```

2. **Crie e ative o ambiente virtual:**

    ```bash
    # Crie o venv
    python -m venv .venv

    # Ative no Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1

    # Ative no Linux/macOS
    # source .venv/bin/activate
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r dev-requirements.txt
    ```

4. **Instale o projeto em modo editável:**

    ```bash
    pip install -e .
    ```

5. **Configurando variáveis de ambiente:**

- Acesse a pasta `config/`.
- Crie uma cópia do arquivo `.env.example` e renomeie-o para `.env`.
- Abra o arquivo `.env` e preencha-o com os valores corretos da sua instância Snipe-IT.

---

## 🛠️ Uso

Com o ambiente virtual ativado, execute a aplicação a partir da raiz do projeto com o seguinte comando:

```bash
python -m src.assets_term_generator
```

O programa o guiará com prompts interativos para inserir o número do funcionário e selecionar o tipo de documento e a categoria do ativo.

---

## ✅ Testes

O projeto utiliza `pytest` para testes automatizados. Para executar o conjunto de testes:

```bash
pytest
```

Para gerar um relatório de cobertura de teste:

```bash
pytest --cov=src
```

---

## 🔧 Personalização de Templates (Jinja2)

Este aplicativo usa **`docxtpl`** para permitir a poderosa linguagem de templates **Jinja2** diretamente dentro dos seus templates `.docx`. Isso significa que você pode adicionar lógica, como condicionais e laços, aos seus documentos sem alterar nenhum código Python.

### As 3 Regras de Ouro das Tags Jinja2

1. **`{{ ... }}` (Chaves Duplas):** Para **MOSTRAR** ou **imprimir** um dado.

   - *Exemplo:* `Nome do Funcionário: {{ user.name }}`

2. **`{% ... %}` (Chaves e Porcentagem):** Para **LÓGICA** e **fluxo de controle**.

   - *Exemplo:* `{% if asset.notes %}` ou `{% for item in asset.accessories %}`

3. **`{# ... #}` (Chaves e Sustenido):** Para **COMENTÁRIOS** que são invisíveis no documento final.

   - *Exemplo:* `{# TODO: Obter aprovação desta cláusula pelo Departamento Jurídico #}`

### Dados Disponíveis em Modelos (Contexto)

Ao criar seu modelo, você tem acesso a estes objetos principais:

#### Objeto `user`

Contém informações sobre o funcionário.

- `user.name`
- `user.employee_num`
- `user.department.name`

#### Objeto `asset`

Contém informações sobre o ativo principal selecionado (por exemplo, o laptop ou smartphone).

- `asset.asset_tag`
- `asset.model.name`
- `asset.serial`
- `asset.category.name`
- `asset.notes`
- `asset.get_custom_field('Nome do Campo')`
- `asset.accessories`: Uma **lista** de todos os objetos acessórios anexados a este ativo.
- `asset.components`: Uma **lista** de todos os objetos componentes anexados a este ativo.

### Exemplos Práticos

#### 1. Exibindo um Parágrafo Condicionalmente

Para exibir uma cláusula apenas para Laptops:

```jinja
{% if asset.category.name == 'Laptops' %}
CLÁUSULA DA BATERIA: Recomenda-se não deixar o equipamento conectado ininterruptamente para preservar a vida útil da bateria.
{% endif %}
```

#### 2. Listando Todos os Acessórios

Para criar automaticamente uma lista de todos os acessórios:

```jinja
Acessórios Adicionais:
{% for item in asset.accessories %}
- {{ item.name }} (Categoria: {{ item.category.name }})
{% else %}
- Nenhum acessório adicional foi fornecido com este equipamento.
{% endfor %}
```

---

## 🏛️ Decisões de Arquitetura e Design

Este projeto segue práticas modernas de desenvolvimento em Python.

- **Lógica em Templates:** Ao usar o Jinja2, a lógica de apresentação (o que mostrar e quando) é movida para os templates `.docx`, desvinculando-a do código Python e permitindo que não desenvolvedores modifiquem as estruturas dos documentos.
- **Camada de Serviço (Fachada)**: A lógica de orquestração de chamadas de API é isolada no módulo `api/snipeit_client.py`, o que oculta a complexidade e entrega objetos de dados Pydantic limpos para a aplicação.
- **Injeção de Dependências**: Componentes como o `DocumentProcessor` recebem suas configurações por meio do construtor (`__init__`), tornando-os desvinculados e mais fáceis de testar.
- **Ferramentas de Qualidade**: `pre-commit` é configurado para executar `ruff` e `mypy` antes de cada commit, garantindo automaticamente a qualidade e a consistência do código.

---

## 📈 Roteiro

- [ ] Desenvolver uma interface web com FastAPI.

---

## 🤝 Contribuindo

Pull requests são bem-vindos. Para alterações maiores, abra uma issue primeiro para discutir o que você gostaria de alterar.

---

## ✍️ Autores

- [@Diogovx](https://github.com/Diogovx)

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**. Consulte o arquivo `LICENSE` para obter detalhes.
