#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MongoDB Write Script

This script demonstrates how to connect to a MongoDB database and insert a document.
It uses environment variables for secure credential management.
"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_mongodb_connection_string():
    """
    Retrieve MongoDB connection parameters from environment variables and
    construct a connection string.
    
    Returns:
        str: MongoDB connection string
    """
    # Get MongoDB credentials from environment variables
    mongo_username = os.getenv('mongo_username')
    mongo_password = os.getenv('mongo_password')
    
    # Validate that credentials are available
    if not mongo_username or not mongo_password:
        print("Error: MongoDB credentials not found in environment variables.")
        print("Make sure you have a .env file with mongo_username and mongo_password defined.")
        sys.exit(1)
    
    # Construct the MongoDB connection string
    return f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/"

def insert_document(client, database_name, collection_name, document_data):
    """
    Insert a document into a MongoDB collection.
    
    Args:
        client (MongoClient): MongoDB client instance
        database_name (str): Name of the database
        collection_name (str): Name of the collection
        document_data (dict): Document to be inserted
        
    Returns:
        dict: The inserted document with its _id
    """
    # Access the specified database and collection
    db = client[database_name]
    collection = db[collection_name]
    
    # Insert the document into the collection
    insert_result = collection.insert_one(document_data)
    print(f"✅ Document inserted with ID: {insert_result.inserted_id}")
    
    # Retrieve and return the inserted document
    return collection.find_one({"_id": insert_result.inserted_id})


def main():
    """
    Main function to demonstrate MongoDB write operations.
    """
    # Get MongoDB connection string
    mongo_url = get_mongodb_connection_string()
    client = None
    
    try:
        # Establish connection to MongoDB
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test the connection with a ping command
        client.admin.command('ping')
        print("✅ Connected to MongoDB!")
        
        # Define database and collection names
        database_name = 'fin'
        collection_name = 'transacoes'
        
        # Define the document to be inserted
        document = {
            "nome": "Exemplo",
            "valor": 123,
            "descricao": "Exemplo de inserção de documento"
        }
        
        # Insert the document and get the result
        captured_document = insert_document(
            client, 
            database_name, 
            collection_name, 
            document
        )
        
        # Display the inserted document in a formatted way
        print("\nInserted document:")
        for key, value in captured_document.items():
            print(f"  {key}: {value}")
            
    except ConnectionFailure as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        print("Please check if MongoDB server is running and accessible.")
        
    except OperationFailure as e:
        print(f"❌ Authentication error: {e}")
        print("Please check your MongoDB credentials in the .env file.")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        # Ensure the connection is closed even if an exception occurs
        if client:
            client.close()
            print("\n✅ MongoDB connection closed.")


# Execute main function when script is run directly
if __name__ == "__main__":
    main()