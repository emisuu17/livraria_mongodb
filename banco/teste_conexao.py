import os
from dotenv import load_dotenv
import pymongo
import certifi  # <--- 1. Importação necessária

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Obtém a URI do MongoDB Atlas do .env
MONGO_URI = os.getenv('MONGO_URI')

print("Tentando conectar...")

try:
    # 2. A CORREÇÃO MÁGICA ESTÁ AQUI: tlsCAFile=certifi.where()
    client = pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    
    # O comando 'ping' é mais rápido e leve para testar a conexão do que listar bancos
    client.admin.command('ping')
    
    print("✅ Conectado ao MongoDB Atlas com sucesso!")
    
    # Agora lista os bancos
    print("Bancos de dados disponíveis:", client.list_database_names())
    
    client.close()

except Exception as e:
    print(f"❌ Erro ao conectar ao MongoDB Atlas: {e}")