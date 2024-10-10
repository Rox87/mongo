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

    # Document to be inserted
    document = {
        "nome": "Exemplo",
        "valor": 123
    }

    # Insert the document into the collection
    insert_result = collection.insert_one(document)
    print(f"Document inserted with ID: {insert_result.inserted_id}")

    # Retrieve the inserted document
    captured_document = collection.find_one({"_id": insert_result.inserted_id})
    print("Captured document:", captured_document)

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

finally:
    # Closing the connection
    client.close()