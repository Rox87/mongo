from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações de conexão do MongoDB a partir das variáveis de ambiente
mongo_username = os.getenv('mongo_username')
mongo_password = os.getenv('mongo_password')

mongo_url = f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/"  # Use the appropriate IP if hostname fails

# Connection to MongoDB
try:
    client = MongoClient(mongo_url)
    # Test the connection
    client.admin.command('ping')
    print("Connected to MongoDB!")

    # Database and collection names
    db = client['fin']  # Replace with your database name
    collection = db['transacoes']  # Replace with your collection name

    # Percorrendo e imprimindo todos os documentos da coleção
    for document in collection.find():
        print(document)

    # imprima somente os elementos de uma query
    query = { "nome": "Exemplo" }
    result = collection.find(query)
    
    for document in result:
        print(document)

except Exception as e:
    print(f"Erro ao acessar a coleção: {e}")
finally:
    # Fechar a conexão com o MongoDB
    client.close()