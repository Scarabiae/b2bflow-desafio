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