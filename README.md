# Gerador de Termos de Responsabilidade de ativos de TI (Snipe-IT)

O Gerador de Termos de Responsabilidade é uma aplicação em Python que automatiza a criação de termos para equipamentos de TI (notebooks e celulares) atribuídos a colaboradores. O sistema consulta as APIs do Snipe-IT para obter os dados dos equipamentos e gera documentos Word (.docx) padronizados.

## Funcionamento do Programa

### Fluxo Principal

1. O usuário informa a matrícula do colaborador.

2. O sistema consulta a API para obter os equipamentos associados.

3. O usuário seleciona o tipo de termo a gerar (Notebook ou Celular).

4. Se houver múltiplos equipamentos do tipo selecionado, o usuário escolhe qual deseja incluir no termo.

5. O sistema gera o documento Word com as informações preenchidas.

6. O documento é salvo no diretório de saída com o nome formatado.

## Exemplo de uso

```bash
? Digite a matrícula: 2639
? Você deseja gerar qual termo?
Escolha um deles:  Notebook
INFO - Template carregado com sucesso
INFO - Ativo selecionado: LATITUDE 5420
INFO - Termo de responsabilidade do usuário Diogo Velozo Xavier criado!
```

## Configurações do ambiente

### 1. Requisitos

- Python 3.8+
- Bibliotecas listadas em `requirements.txt`

### 2. Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env.
    `API_HARDWARE_URL`
    `API_USERS_URL`
    `API_ACESSORIES_URL`
    `API_KEY`

#### .env de exemplo

```.env
API_HARDWARE_URL=https://sua-api.com/api/v1/hardware
API_USERS_URL=https://sua-api.com/api/v1/users
API_ACESSORIES_URL=https://sua-api.com/api/v1/accessories
API_KEY=123456789abcdef
```

### 3. Template

- Coloque os templates em `docx-template/TERMO DE RESPONSABILIDADES {Tipo}.docx` (onde `{Tipo}` pode ser NOTEBOOKS ou CELULARES).
- Certifique-se de incluir todos os marcadores necessários; eles estão listados no arquivo `document_processor.py`.

## Tratamento de erros e logs

### Erros

- Caso a matrícula informada não exista no sistema, uma mensagem de erro será exibida no terminal.
- Caso o colaborador não possua equipamentos do tipo selecionado, o programa exibe um erro amigável e retorna ao menu inicial.

#### Mensagens de erro comuns

- `Erro de seleção: Nenhum ativo do tipo Smartphones encontrado`  
  O colaborador não possui ativos da categoria selecionada.

- `Erro ao processar termo: Resposta inválida da API`  
  A API pode estar offline ou o token de autenticação está incorreto.

- `Matrícula não pode ser vazia`  
  O campo da matrícula precisa ser preenchido.

- `Usuário com matrícula XXXXX não encontrado`  
  Nenhum ativo foi associado a esse número de matrícula.

### Logs

- Os logs são armazenados em `logs/termo_responsabilidade.log`
- Eles estão no nível `INFO` e `ERROR`

## Testes

Este projeto não possui testes automatizados, mas recomenda-se:

- Testar com um usuário com múltiplos ativos.
- Testar com um usuário sem ativos.
- Testar ausência de template.

## Deploy

1. Para fazer o deploy desse projeto instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

2. Execute o programa:

    ```bash
    python main.py 
    ```

3. Siga as instruções no terminal para gerar os termos.

## Documentação da API

### Retorna todos os ativos

```http
  GET /api/v1/hardware
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `api_key` | `string` | **Obrigatório**. A chave da sua API |

### Retorna todos os acessórios

```http
  GET /api/v1/accessories
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `api_key`      | `string` | **Obrigatório**. A chave da sua API |

### Funções para manipular as APIs

#### hardware_api_call(assigned_to)

Função responsável por consultar a API de ativos e selecionar os equipamentos de um usuário específico. Implementada em `api_call.py`

#### accessories_api_call(user_id)

Função responsável por consultar a API de acessórios e selecionar os itens de um usuário específico. Também está localizada em `api_call.py`

## Melhorias

- Implementação de uma interface gráfica para facilitar o uso.
- Histórico de termos gerados
- Integração direta com e-mail para envio automático do termo
- Geração de PDFs
- Testes automatizados com pytest
- Dockerização para facilitar o deploy

## Contribuindo

Pull requests são bem-vindos. Para mudanças maiores, por favor abra uma issue para discussão prévia.

## Autores

- [@Diogovx](http://github.com/Diogovx)

## Licença

Este projeto está atualmente sem uma licença específica. Considere adicionar uma como MIT, GPLv3, ou Apache 2.0.
