# Manual do Usuário - Gerador de Termos de Responsabilidade

Bem-vindo! Este programa ajuda você a criar termos de responsabilidade para equipamentos de TI de forma rápida e automática.

## Requisitos

- Computador com sistema operacional Windows.

## ⚙️ Configuração Inicial (Feita apenas uma vez)

Antes de usar o programa pela primeira vez, você precisa configurar suas informações de acesso à API.

1. **Abra a pasta `config`** que está junto com este manual.
2. Dentro dela, você encontrará um arquivo chamado `.env`. **Abra este arquivo com o Bloco de Notas**.
3. Você verá um texto parecido com este:

    ```env
    API_KEY="SUA_CHAVE_DE_API_GERADA_NO_SNIPE_IT"
    API_USERS_URL="http://seu-snipe-it/api/v1/users"
    API_HARDWARE_URL="http://seu-snipe-it/api/v1/hardware"
    API_ACCESSORIES_URL="http://seu-snipe-it/api/v1/accessories"
    API_COMPONENTS_URL="http://seu-snipe-it/api/v1/components"
    ```

4. **Substitua os textos de exemplo** pelos valores corretos da sua empresa. Por exemplo, troque `"SUA_CHAVE_DE_API_GERADA_NO_SNIPE_IT"` pela sua chave real.
5. **Salve e feche** o arquivo.

Pronto! A configuração está concluída.

## ▶️ Como Usar o Programa

1. Dê um **clique duplo** no arquivo `Assets_term_generator.exe`.
2. Uma tela de terminal preta irá se abrir.
3. Siga as instruções que aparecerem na tela:
    - Digite a **matrícula** do colaborador e pressione Enter.
    - Use as setas do teclado para **selecionar o tipo de termo** (Notebook, Celular, etc.) e pressione Enter.
    - Se necessário, selecione o equipamento específico.
4. Ao final do processo, um documento Word será criado e aberto automaticamente para você.
5. O arquivo `.docx` gerado fica salvo na pasta `output`.

## ❓ Solução de Problemas Comuns

- **"O programa pisca na tela e fecha"**:
  - Verifique se você preencheu corretamente o arquivo `.env` na pasta `config`. Qualquer erro de digitação nas URLs ou na chave da API pode causar isso.
  - Certifique-se de que seu computador tem acesso à internet e consegue se comunicar com o sistema Snipe-IT.

- **"Usuário não encontrado" ou "Ativo não encontrado"**:
  - Verifique se a matrícula digitada está correta e se o usuário realmente possui aquele tipo de equipamento associado a ele no sistema Snipe-IT.

Para qualquer outro problema, por favor, entre em contato com o suporte de TI.

## 📋 Histórico de Geração

Para fins de auditoria e controle, toda vez que um termo é gerado com sucesso, o programa registra um evento em um arquivo de histórico.

Este histórico é um arquivo chamado `generation_history.csv` e está localizado dentro da pasta `logs`. Você pode abrir este arquivo diretamente com o Microsoft Excel para visualizar, filtrar e criar relatórios sobre os termos gerados.

Cada linha no histórico contém as seguintes informações:

- **timestamp**: A data e hora exatas em que o termo foi gerado.
- **user_generator**: O nome de usuário do computador da pessoa que gerou o termo.
- **employee_number**: A matrícula do colaborador para quem o termo foi feito.
- **employee_name**: O nome completo do colaborador.
- **asset_tag**: A asset tag do equipamento principal descrito no termo.
- **modelo_ativo**: O modelo do equipamento principal.
- **user_template**: O tipo de termo que foi gerado (ex: `laptops`, `smartphones`).
- **generated_term_path**: O local exato no computador onde o arquivo `.docx` final foi salvo.

## 🔧 Personalizando os Templates (Avançado)

Com o novo sistema, você tem total controle para criar e modificar os templates diretamente no Microsoft Word. A "inteligência" de como os dados são exibidos agora vive dentro do próprio documento, usando um sistema de **etiquetas inteligentes**.

### As 3 Regras de Ouro das Etiquetas

Existem 3 tipos de etiquetas especiais que você pode usar no seu documento `.docx`:

1. **`{{ ... }}` (Chaves Duplas):** Para **MOSTRAR** uma informação.
    - Exemplo: `O nome do colaborador é {{ user.name }}`.

2. **`{% ... %}` (Chave e Porcentagem):** Para **LÓGICA**, como criar listas ou mostrar um parágrafo apenas se uma condição for verdadeira.
    - Exemplo: `{% for item in asset.accessories %}`.

3. **`{# ... #}` (Chave e Jogo da Velha):** Para **COMENTÁRIOS** que não aparecerão no documento final.
    - Exemplo: `{# TODO: Pedir ao Jurídico para revisar esta cláusula #}`.

---

### Dicionário de Dados (Sua "Cola")

Aqui estão as principais informações que você pode usar nos seus templates.

#### Objeto `user` (Informações do Colaborador)

| Para Inserir... | Use a Etiqueta |
| :--- | :--- |
| Nome Completo | `{{ user.name }}` |
| Matrícula | `{{ user.employee_num }}` |
| Departamento | `{{ user.department.name }}` |

#### Objeto `asset` (O Equipamento Principal)

| Para Inserir... | Use a Etiqueta |
| :--- | :--- |
| Asset Tag | `{{ asset.asset_tag }}` |
| Nome do Modelo | `{{ asset.model.name }}` |
| Número de Série | `{{ asset.serial }}` |
| Nome da Categoria | `{{ asset.category.name }}` |
| Anotações | `{{ asset.notes }}` |
| Campo Customizado | `{{ asset.get_custom_field('NOME_DO_CAMPO') }}` |

---

### Exemplos Práticos

#### **1. Mostrar um parágrafo apenas se uma condição for verdadeira**

Você quer que uma cláusula sobre "cuidados com a bateria" apareça apenas para notebooks? Use um bloco `if`.

**Exemplo no Word:**

```jinja
{% if asset.category.name == 'Laptops' %}
CLÁUSULA DE BATERIA: Recomenda-se não deixar o equipamento conectado na tomada ininterruptamente para preservar a vida útil da bateria.
{% endif %}
```

*O parágrafo inteiro só aparecerá se a categoria do ativo principal for "Laptops".*

#### **2. Criar uma lista automática de itens**

Esta é a funcionalidade mais poderosa. Você pode criar uma lista de todos os acessórios ou componentes associados.

**Exemplo no Word:**

```jinja
Lista de Acessórios Adicionais:
{% for item in asset.accessories %}
- {{ item.name }} (Categoria: {{ item.category.name }})
{% else %}
- Nenhum acessório adicional foi entregue com este equipamento.
{% endfor %}
```

- **O que isso faz:** O `{% for ... %}` cria uma nova linha para cada acessório. O `{% else %}` mostra uma mensagem padrão se a lista de acessórios estiver vazia.

---

### ❓ Solucionando Erros Comuns nos Templates

Se o programa der um erro ao gerar o documento, geralmente é um erro de digitação no template.

- **Erro `Encountered unknown tag 'user'`:**
  - **Causa:** Você provavelmente escreveu `{% user.name %}` em vez de `{{ user.name }}`.
  - **Solução:** Lembre-se, para **mostrar** dados, use sempre chaves duplas `{{ }}`.

- **Erro `unexpected '%'`:**
  - **Causa:** Você provavelmente usou um caractere `%` em um texto normal (ex: "Bateria com 100% de carga") dentro de um bloco `{% if ... %}`.
  - **Solução:** Envolva o texto problemático com as tags `{% raw %}` e `{% endraw %}` para que o sistema o ignore.

      ```jinja
      {% raw %}Texto com % que causa problema.{% endraw %}
      ```

- **O placeholder aparece em branco no documento final:**
  - **Causa:** O nome da variável está errado. Você pode ter digitado `{{ user.nome }}` em vez de `{{ user.name }}.`
  - **Solução:** Consulte o "Dicionário de Dados" acima para usar o nome exato do campo.

## 🔧 Configurando a Aplicação (`config.yml`)

O arquivo `config.yml`, localizado na pasta `config`, é o painel de controle principal do programa. É aqui que você define quais "tipos de termo" a aplicação pode gerar.

### Estrutura Geral

O arquivo é dividido em seções simples:

#### Seção `ui`

Controla a aparência da interface do programa no terminal.

- **`theme`**: Define o tema de cores. Pode ser `dark` (escuro) ou `light` (claro).
- **`logo_path`**: O caminho para a imagem do logo que aparece na interface (atualmente não implementado).

#### Seção `document`

Controla tudo sobre a geração dos documentos.

- **`template_path`**: A pasta onde seus arquivos de modelo `.docx` estão guardados. O padrão é `docx-template/`.
- **`templates`**: Um dicionário com todos os "tipos de documento" que o programa pode criar.

---

### Tutorial: Como Adicionar um Novo Tipo de Termo

Imagine que você precisa criar um novo "Termo de Confidencialidade". O processo é feito em 2 passos, sem precisar de programação.

#### Passo 1: Crie o Template no Word

1. Crie um novo arquivo `.docx` chamado, por exemplo, `TERMO_CONFIDENCIALIDADE.docx`.
2. Escreva todo o texto e adicione as **etiquetas inteligentes (Jinja2)** que precisar (ex: `{{ user.name }}`, `{{ asset.asset_tag }}`, etc.).
3. Salve este arquivo na pasta `docx-template/`.

#### Passo 2: Registre o Novo Template no `config.yml`

1. Abra o arquivo `config.yml` com um editor de texto.
2. Dentro da seção `document` -> `templates`, adicione uma nova entrada para o seu termo.

**Exemplo de adição:**

```yaml
document:
  template_path: docx-template/
  templates:
    termo_de_responsabilidade:
      file_name: TERMO_MESTRE_RESPONSABILIDADE.docx
      description: "Gera o termo padrão de recebimento de ativos."
      # ...

    termo_confidencialidade:
      file_name: TERMO_CONFIDENCIALIDADE.docx
      description: "Gera o termo de confidencialidade para projetos especiais."
      target_categories: # Opcional: restringe a quais categorias de ativos este termo se aplica
        - Laptops
```

**Pronto!** Na próxima vez que você rodar o programa, a opção "Gera o termo de confidencialidade para projetos especiais." aparecerá automaticamente no menu de seleção de documentos.

#### Entendendo as Chaves de um Template

- **`termo_confidencialidade:`**: Este é o "ID" do seu novo termo. O nome é você quem escolhe.
- **`file_name`**: **Obrigatório.** O nome exato do arquivo `.docx` que você criou.
- **`description`**: **Obrigatório.** O texto amigável que aparecerá no menu para o usuário selecionar.
- **`target_categories`**: **Opcional.** Uma lista de categorias de ativos para as quais este termo pode ser aplicado. Se você omitir esta chave, o termo poderá ser aplicado a qualquer tipo de ativo.
