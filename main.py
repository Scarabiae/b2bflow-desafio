import os
import logging
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

# --- Configuração Inicial ---
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura um logging básico para registrar informações e erros
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Carregamento das Variáveis de Ambiente ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")

# Validação para garantir que todas as variáveis foram carregadas
if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE_ID, ZAPI_TOKEN]):
    logging.error("Erro: Variáveis de ambiente não foram carregadas corretamente. Verifique seu arquivo .env.")
    exit() # Encerra o script se as variáveis não estiverem presentes

# --- Funções ---

def get_supabase_contacts(supabase_client: Client) -> list:
    """
    Busca os contatos cadastrados na tabela 'contatos' do Supabase.
    """
    try:
        logging.info("Buscando contatos no Supabase...")
        response = supabase_client.table('contatos').select("nome_contato, telefone").execute()
        
        # A API do Supabase retorna os dados dentro de um objeto 'data'
        if response.data:
            logging.info(f"{len(response.data)} contatos encontrados.")
            return response.data
        else:
            logging.warning("Nenhum contato encontrado na tabela do Supabase.")
            return []
            
    except Exception as e:
        logging.error(f"Erro ao buscar contatos no Supabase: {e}")
        return []

def send_whatsapp_message(contact_name: str, contact_phone: str):
    """
    Envia uma mensagem de WhatsApp para um contato específico via Z-API.
    """
    message = f"Olá {contact_name}, tudo bem com você?"
    
    # O endpoint da Z-API para envio de texto
    api_url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    
    payload = {
        "phone": contact_phone,
        "message": message
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        logging.info(f"Enviando mensagem para {contact_name} ({contact_phone})...")
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()
        
        logging.info(f"Mensagem enviada com sucesso para {contact_name}. Status: {response.status_code}")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para {contact_name}: {e}")
        if e.response is not None:
            logging.error(f"Detalhes do erro da API: {e.response.text}")
        return False

def main():
    """
    Função principal que orquestra o fluxo de trabalho.
    """
    logging.info("Iniciando o processo de envio de mensagens...")
    
    try:
        # Inicializa o cliente do Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logging.error(f"Falha ao inicializar o cliente Supabase: {e}")
        return

    contacts = get_supabase_contacts(supabase)
    
    if not contacts:
        logging.info("Nenhum contato para processar. Encerrando.")
        return

    success_count = 0
    error_count = 0

    for contact in contacts:
        contact_name = contact.get('nome_contato')
        contact_phone = contact.get('telefone')

        if not contact_name or not contact_phone:
            logging.warning(f"Registro de contato incompleto, pulando: {contact}")
            error_count += 1
            continue

        if send_whatsapp_message(contact_name, contact_phone):
            success_count += 1
        else:
            error_count += 1
    
    logging.info("--- Resumo do Processo ---")
    logging.info(f"Mensagens enviadas com sucesso: {success_count}")
    logging.info(f"Falhas no envio: {error_count}")
    logging.info("Processo finalizado.")


if __name__ == "__main__":
    main()