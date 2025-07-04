# Gerador de Termos de Responsabilidade de ativos de TI (Snipe-IT)

[![CI de Qualidade e Testes](https://github.com/Diogovx/Asset-term-generator/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/Diogovx/Asset-term-generator/actions/workflows/ci-pipeline.yml)
[![Licença MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

O Gerador de Termos de Responsabilidade é uma aplicação em Python que automatiza a criação de termos para equipamentos de TI (notebooks e celulares) atribuídos a colaboradores. O sistema consulta as APIs do Snipe-IT para obter os dados dos equipamentos e gera documentos Word (.docx) padronizados.

## Sumário

- [Gerador de Termos de Responsabilidade de ativos de TI (Snipe-IT)](#gerador-de-termos-de-responsabilidade-de-ativos-de-ti-snipe-it)
  - [Sumário](#sumário)
  - [Features](#features)
  - [🚀 Instalação e Configuração (Ambiente de Desenvolvimento)](#-instalação-e-configuração-ambiente-de-desenvolvimento)
  - [🛠️ Usage](#️-usage)
  - [✅ Testes](#-testes)
  - [Arquitetura](#arquitetura)
  - [📈 Roadmap de Melhorias](#-roadmap-de-melhorias)
  - [🤝 Contribuindo](#-contribuindo)
  - [✍️ Autores](#️-autores)
  - [📄 Licença](#-licença)

## Features

- **Busca Inteligente:** Encontra usuários pela matrícula e busca todos os seus ativos associados (equipamentos, componentes e acessórios).
- **Geração Dinâmica:** Utiliza templates `.docx` para gerar documentos padronizados e preenchidos automaticamente.
- **Arquitetura Robusta:** Construído com Pydantic para validação de dados, garantindo a integridade das informações da API.
- **Qualidade Garantida:** Pipeline de CI/CD com GitHub Actions para rodar testes (`pytest`) e análise de código (`ruff`, `mypy`) automaticamente.
- **Ambiente Reprodutível:** Gestão de dependências com `pip-tools` para garantir que o ambiente de desenvolvimento seja consistente.

## 🚀 Instalação e Configuração (Ambiente de Desenvolvimento)

Siga estes passos para configurar o ambiente de desenvolvimento em sua máquina.

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/Diogovx/Asset-term-generator.git
    cd Asset-term-generator
    ```

2. **Crie e ative o ambiente virtual:**

    ```bash
    # Crie a venv
    python -m venv .venv

    # Ative no Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1

    # Ative no Linux/macOS
    # source .venv/bin/activate
    ```

3. **Instale as dependências:**
    Este comando instala todas as bibliotecas da aplicação e as ferramentas de desenvolvimento.

    ```bash
    pip install -r dev-requirements.txt
    ```

4. **Instale o projeto em modo editável:**
    Este passo crucial torna seu pacote `assets_term_generator` importável no seu ambiente.

    ```bash
    pip install -e .
    ```

5. **Configure as variáveis de ambiente:**

    - Vá para a pasta `config/`.
    - Renomeie o arquivo `.env.example` para `.env`.
    - Abra o `.env` e preencha com os valores corretos da sua instância do Snipe-IT.

    **Arquivo `config/.env.example`:**

    ```env
    API_KEY="SUA_CHAVE_DE_API_GERADA_NO_SNIPE_IT"
    API_USERS_URL="http://seu-snipe-it/api/v1/users"
    API_HARDWARE_URL="http://seu-snipe-it/api/v1/hardware"
    API_ACCESSORIES_URL="http://seu-snipe-it/api/v1/accessories"
    API_COMPONENTS_URL="http://seu-snipe-it/api/v1/components"
    ```

## 🛠️ Usage

Com o ambiente virtual ativado, execute a aplicação a partir da raiz do projeto com o seguinte comando:

```bash
python -m assets_term_generator
```

O programa irá guiá-lo com prompts interativos para inserir a matrícula e selecionar o tipo de termo.

## ✅ Testes

O projeto utiliza `pytest` para testes automatizados. Para rodar a suíte de testes:

```bash
pytest
```

Para gerar um relatório de cobertura de testes, rode:

```bash
pytest --cov=src
```

## Arquitetura

Este projeto foi refatorado para seguir práticas modernas de desenvolvimento em Python.

- **Modelagem com Pydantic**: Em vez de dicionários, usamos modelos Pydantic (`core/models.py`) para definir "contratos de dados" para a resposta da API e para o `config.yml`. Isso garante validação, conversão de tipos e torna o código mais seguro e autodocumentado.

- **Camada de Serviço (Facade)**: A lógica de orquestração das chamadas à API está isolada no módulo `api/snipeit_client.py`. Ele atua como uma fachada, escondendo a complexidade de múltiplas chamadas e da "costura" dos dados, e entregando objetos Pydantic limpos para o resto da aplicação.

- **Injeção de Dependência**: Componentes como a UI (`Menu`) e o `DocumentProcessor` recebem suas configurações via construtor (`__init__`) em vez de lerem arquivos por conta própria. Isso os desacopla e os torna mais fáceis de testar.

- **Ferramentas de Qualidade**: O `pre-commit` está configurado para rodar `ruff` (linter e formatador) e `mypy` (verificador de tipos) antes de cada commit, garantindo a consistência e a qualidade do código de forma automática.

Este projeto segue o layout `src` para uma clara separação entre o código-fonte e os arquivos de configuração.

- `src/assets_term_generator/`: Contém todo o código-fonte do pacote Python.
  - `api/`: Lógica de comunicação com a API do Snipe-IT.
  - `core/`: O cérebro da aplicação, incluindo o `DocumentProcessor` e os modelos Pydantic.
  - `ui/`: Lógica para a interface de linha de comando.
  - `util/`: Funções de utilidade, como configuração de logs e exceções customizadas.
- `config/`: Arquivos de configuração da aplicação.
- `docx-template/`: Templates `.docx` usados para gerar os termos.
- `tests/`: Testes automatizados.

## 📈 Roadmap de Melhorias

- [ ] Implementar ferramentas de análise de segurança (`bandit`, `pip-audit`) na pipeline de CI.
- [ ] Migrar a geração de documentos para `docxtpl` para permitir lógica condicional e loops (`if`/`for`) diretamente nos templates `.docx`.
- [ ] Desenvolver uma interface web com FastAPI.
- [ ] Adicionar um histórico de termos gerados.

## 🤝 Contribuindo

Pull requests são bem-vindos. Para mudanças maiores, por favor abra uma issue para discussão prévia.

## ✍️ Autores

- [@Diogovx](http://github.com/Diogovx)

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.
