# Desafio de Estágio b2bflow - Notificador de WhatsApp

Este projeto é uma solução para o desafio da b2bflow, que consiste em criar um script Python para ler contatos de um banco de dados Supabase e enviar uma mensagem personalizada via Z-API.

## Funcionalidades

-   Lê uma lista de contatos (nome e telefone) de uma tabela no Supabase.
-   Envia uma mensagem de WhatsApp personalizada para cada contato.
-   Utiliza variáveis de ambiente para gerenciar chaves de API de forma segura.
-   Inclui logs para acompanhar o processo de execução.

---

### 🛠️ Setup do Projeto

**1. Tabela no Supabase**

Você precisa criar uma tabela no seu projeto Supabase com a seguinte estrutura:

-   Nome da Tabela: `contatos`
-   Colunas:
    -   `id` (int8, primary key)
    -   `nome_contato` (text)
    -   `telefone` (text) - *Armazene com o código do país e DDD, ex: 55119XXXXXXXX*

**2. Variáveis de Ambiente**

Crie um arquivo chamado `.env` na raiz do projeto e preencha com suas credenciais:

```ini
# Variáveis do Supabase
SUPABASE_URL="SUA_URL_DO_PROJETO_SUPABASE"
SUPABASE_KEY="SUA_CHAVE_PUBLICA_ANON_DO_SUPABASE"

# Variáveis da Z-API
ZAPI_INSTANCE_ID="SEU_ID_DA_INSTANCIA_ZAPI"
ZAPI_TOKEN="SEU_TOKEN_DA_ZAPI"
```

---

### 🚀 Como Rodar

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd desafio-b2bflow
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o script:**
    ```bash
    python main.py
    ```

O terminal exibirá logs informando sobre o processo de busca e envio das mensagens.

## Status Atual e Depuração do Erro 403

O código foi implementado para cumprir todos os requisitos do desafio. O fluxo de leitura do Supabase funciona perfeitamente. No entanto, a etapa final de envio de mensagem pela Z-API está sendo bloqueada por um erro persistente `403 Forbidden`, com a mensagem da API sendo `{"error":"Client-Token ... not allowed"}`.

Acredito que se trata de uma restrição ou instabilidade na conta de teste da Z-API, e não um erro no código da aplicação. Para chegar a essa conclusão, foram realizados os seguintes passos de depuração:

-   **Testes de Conexão Isolados:**
    -   Um script (`test_supabase.py`) foi criado para testar apenas a conexão com o Supabase, que obteve **sucesso**.
    -   Um script (`test_zapi.py`) foi criado para testar apenas a Z-API, que apresentou o mesmo erro, isolando a causa.

-   **Análise do Código e Ambiente:**
    -   Verificação do `Client-Token` no cabeçalho da requisição via `print`s de depuração, que confirmaram que o header estava sendo montado corretamente.
    -   Correção de formatação de caracteres "invisíveis" no código.
    -   Correção do arquivo `.env` para remover aspas nos valores das variáveis.

-   **Ações na Plataforma Z-API:**
    -   Criação de uma **nova instância e um novo token** para descartar a possibilidade de um token corrompido.
    -   Liberação (whitelist) do IP público de execução no painel de segurança da Z-API e aguardo do tempo de propagação.

Após todas essas etapas, o erro `403` persistiu, indicando que a causa é externa ao projeto. O código está funcional e pronto para operar assim que a permissão na API for estabelecida.