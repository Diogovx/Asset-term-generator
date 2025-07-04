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

## 🔧 Personalizando os Termos (`config.yml`)

O arquivo `config.yml`, localizado na pasta `config`, é o cérebro da geração de documentos. Ele permite que você adicione novos tipos de termos ou personalize os placeholders existentes.

### Estrutura Geral

O arquivo é dividido em duas seções principais: `ui` e `document`.

#### Seção `ui`

Controla a aparência da interface do programa.

- **`theme`**: Define o tema de cores. Pode ser `dark` (escuro) ou `light` (claro).
- **`logo_path`**: O caminho para a imagem do logo que aparece na interface.

---

#### Seção `document`

Controla tudo sobre a geração dos documentos Word.

- **`template_path`**: A pasta onde seus arquivos de modelo `.docx` estão guardados.
- **`templates`**: Uma lista de todos os tipos de termos que podem ser gerados (ex: `laptops`, `smartphones`).

  - **`file_name`**: O nome exato do arquivo `.docx` correspondente a este termo.
  - **`placeholders`**: A lista de todas as "etiquetas" que serão substituídas dentro daquele documento.

- **`default_placeholders`**: Uma lista de placeholders que são comuns a **todos** os termos, como o nome e a matrícula do colaborador.

---

### Entendendo um `placeholder`

Cada item na lista de `placeholders` é uma "etiqueta" que o programa irá substituir. Ele possui várias chaves que definem seu comportamento:

- **`name`**: O texto exato do placeholder no documento Word. Ex: `[LAPTOPMODEL]`.
- **`type`**: O tipo de dado. Geralmente `text`.
- **`category`**: A categoria do ativo no Snipe-IT à qual este placeholder se refere. Ex: `"Laptops"`, `"Mouses"`, `"SIM Card"`. **É crucial que este nome seja idêntico ao nome da categoria no Snipe-IT.**
- **`description`**: Uma breve descrição do que este placeholder representa.
- **`required`**: Se for `true`, o programa irá gerar um erro caso não encontre um valor para este placeholder. Se for `false`, ele simplesmente deixará o espaço em branco.
- **`identifier`**: Se for `true`, indica que este campo é o principal identificador do usuário (no caso, a matrícula).
- **`generates_presence_marker`**: Se for `true`, o programa também procurará por um placeholder de presença (ex: `[HASLAPTOP]`) e o preencherá com o `presence_marker_value`.
- **`presence_marker_value`**: O texto a ser usado no marcador de presença (geralmente `"X"`).
- **`source`**: **A parte mais importante.** Diz ao programa de onde buscar a informação.
  - **`type`**: Define a origem do dado. Pode ser:
    - `text`: Busca um atributo do objeto **usuário**.
    - `asset`: Busca um atributo do **ativo principal**.
    - `accessories`: Busca na lista de **acessórios** do ativo.
    - `components`: Busca na lista de **componentes** do ativo.
  - **`path`**: Usado com `type: text`, `accessories` ou `components`. É o nome exato do campo a ser extraído do objeto correspondente (ex: `name`, `serial`, `employee_num`).
  - **`format`**: Usado com `type: asset` ou para valores compostos. Permite criar um texto combinando múltiplos dados.
    - Ex: `format: "{model} - {asset_tag}"` irá juntar o nome do modelo com a asset tag.
    - Ex: `format: "{item.name} - {asset.get_custom_field('NUMERO')}"` pega o nome de um componente (`item.name`) e o combina com um campo customizado do ativo pai.
