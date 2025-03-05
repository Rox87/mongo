#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MongoDB Read Script

This script demonstrates how to connect to a MongoDB database and query documents.
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

def print_all_documents(collection):
    """
    Print all documents in a collection.
    
    Args:
        collection: MongoDB collection object
    """
    print("\n📄 All documents in collection:")
    documents = list(collection.find())
    
    if not documents:
        print("  No documents found in the collection.")
        return
        
    for i, document in enumerate(documents, 1):
        print(f"\n  Document {i}:")
        for key, value in document.items():
            print(f"    {key}: {value}")


def query_documents(collection, query):
    """
    Query and print documents matching specific criteria.
    
    Args:
        collection: MongoDB collection object
        query (dict): Query criteria
    """
    print(f"\n🔍 Documents matching query: {query}")
    documents = list(collection.find(query))
    
    if not documents:
        print(f"  No documents found matching the query.")
        return
        
    for i, document in enumerate(documents, 1):
        print(f"\n  Result {i}:")
        for key, value in document.items():
            print(f"    {key}: {value}")


def main():
    """
    Main function to demonstrate MongoDB read operations.
    """
    # Get MongoDB connection string
    mongo_url = get_mongodb_connection_string()
    client = None
    
    try:
        # Establish connection to MongoDB with timeout
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test the connection with a ping command
        client.admin.command('ping')
        print("✅ Connected to MongoDB!")
        
        # Define database and collection names
        database_name = 'fin'
        collection_name = 'transacoes'
        
        # Access the specified database and collection
        db = client[database_name]
        collection = db[collection_name]
        
        # Print all documents in the collection
        print_all_documents(collection)
        
        # Query and print documents matching specific criteria
        query = {"nome": "Exemplo"}
        query_documents(collection, query)
            
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