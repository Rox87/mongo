#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MongoDB Launch Script

This script manages the MongoDB environment using Docker Compose.
It handles starting/stopping the MongoDB and Mongo Express containers.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def check_docker():
    """
    Check if Docker is running and available.
    
    Returns:
        bool: True if Docker is running, False otherwise
    """
    try:
        subprocess.run(['docker', 'info'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_compose_file_path():
    """
    Get the path to the Docker Compose file.
    
    Returns:
        Path: Path to the docker-compose.yml file
    """
    script_dir = Path(__file__).parent
    compose_file = script_dir / 'container' / 'mongo.yml'
    
    if not compose_file.exists():
        print(f"❌ Error: Docker Compose file not found at {compose_file}")
        sys.exit(1)
        
    return compose_file

def start_containers(compose_file):
    """
    Start the MongoDB containers using Docker Compose.
    
    Args:
        compose_file (Path): Path to the docker-compose.yml file
    """
    try:
        print("🚀 Starting MongoDB containers...")
        subprocess.run(
            ['docker', 'compose', '-f', str(compose_file), 'up', '-d'],
            check=True
        )
        print("✅ Containers started successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting containers: {e}")
        sys.exit(1)

def check_container_health():
    """
    Check if the containers are healthy and running.
    """
    try:
        # Wait a bit for containers to initialize
        print("⏳ Waiting for containers to initialize...")
        time.sleep(5)
        
        # Check MongoDB container
        mongo_status = subprocess.run(
            ['docker', 'compose', 'ps', 'mongo', '--format', 'json'],
            capture_output=True,
            text=True
        )
        
        # Check Mongo Express container
        express_status = subprocess.run(
            ['docker', 'compose', 'ps', 'mongo-express', '--format', 'json'],
            capture_output=True,
            text=True
        )
        
        if 'running' in mongo_status.stdout.lower():
            print("✅ MongoDB is running!")
            print("   → Available at: mongodb://localhost:27017")
        else:
            print("❌ MongoDB container is not running properly")
        
        if 'running' in express_status.stdout.lower():
            print("✅ Mongo Express is running!")
            print("   → Web Interface: http://localhost:8081")
        else:
            print("❌ Mongo Express container is not running properly")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking container status: {e}")

def main():
    """
    Main function to launch MongoDB environment.
    """
    print("\n🔄 Initializing MongoDB Environment...\n")
    
    # Check if Docker is running
    if not check_docker():
        print("❌ Error: Docker is not running or not installed.")
        print("Please start Docker and try again.")
        sys.exit(1)
    
    # Get the compose file path
    compose_file = get_compose_file_path()
    
    # Start the containers
    start_containers(compose_file)
    
    # Check container health
    check_container_health()
    
    print("\n✨ MongoDB environment is ready!")
    print("→ Use the MongoDB connection string from your .env file to connect")
    print("→ Access Mongo Express at http://localhost:8081")

if __name__ == "__main__":
    main()