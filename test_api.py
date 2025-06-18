#!/usr/bin/env python3
"""
Test script for the Manufacturing REST API
This script demonstrates how to use the REST API endpoints
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api/v1"

def print_response(response, title=""):
    """Pretty print API response"""
    print(f"\n{'='*50}")
    if title:
        print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_demo_endpoint():
    """Test the demonstration endpoint"""
    print("\n🔍 Testing Demo Endpoint...")
    response = requests.get(f"{BASE_URL}/api/demo")
    print_response(response, "Demo Endpoint Response")

def test_api_documentation():
    """Test the API documentation endpoint"""
    print("\n📚 Testing API Documentation...")
    response = requests.get(f"{API_BASE}/docs")
    print_response(response, "API Documentation")

def test_contacts_api():
    """Test contacts API endpoints"""
    print("\n👥 Testing Contacts API...")
    
    # Get all contacts
    response = requests.get(f"{API_BASE}/contacts")
    print_response(response, "Get All Contacts")
    
    if response.status_code == 200:
        contacts = response.json()
        if contacts:
            # Get specific contact
            contact_id = contacts[0]['id']
            response = requests.get(f"{API_BASE}/contacts/{contact_id}")
            print_response(response, f"Get Contact {contact_id}")

def test_wires_api():
    """Test wires API endpoints"""
    print("\n🔌 Testing Wires API...")
    
    # Get all wires
    response = requests.get(f"{API_BASE}/wires")
    print_response(response, "Get All Wires")
    
    if response.status_code == 200:
        wires = response.json()
        if wires:
            # Get specific wire
            wire_id = wires[0]['id']
            response = requests.get(f"{API_BASE}/wires/{wire_id}")
            print_response(response, f"Get Wire {wire_id}")

def test_processes_api():
    """Test processes API endpoints"""
    print("\n⚙️ Testing Processes API...")
    
    # Get all processes
    response = requests.get(f"{API_BASE}/processes")
    print_response(response, "Get All Processes")
    
    if response.status_code == 200:
        processes = response.json()
        if processes:
            # Get specific process
            process_id = processes[0]['id']
            response = requests.get(f"{API_BASE}/processes/{process_id}")
            print_response(response, f"Get Process {process_id}")

def test_recipes_api():
    """Test recipes API endpoints"""
    print("\n📋 Testing Recipes API...")
    
    # Get all recipes
    response = requests.get(f"{API_BASE}/recipes")
    print_response(response, "Get All Recipes")
    
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            # Get specific recipe
            recipe_id = recipes[0]['id']
            response = requests.get(f"{API_BASE}/recipes/{recipe_id}")
            print_response(response, f"Get Recipe {recipe_id}")

def test_create_and_delete():
    """Test creating and deleting a test job"""
    print("\n➕ Testing Create and Delete Operations...")
    
    # Create a test job
    test_job = {
        "name": f"Test Job {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "status": "pending"
    }
    
    response = requests.post(
        f"{API_BASE}/jobs",
        json=test_job,
        headers={'Content-Type': 'application/json'}
    )
    print_response(response, "Create Test Job")
    
    if response.status_code == 201:
        job_data = response.json()
        job_id = job_data['id']
        
        # Update the job
        update_data = {"status": "completed"}
        response = requests.put(
            f"{API_BASE}/jobs/{job_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        print_response(response, f"Update Job {job_id}")
        
        # Delete the job
        response = requests.delete(f"{API_BASE}/jobs/{job_id}")
        print_response(response, f"Delete Job {job_id}")

def test_device_commands():
    """Test device commands API"""
    print("\n🎮 Testing Device Commands...")
    
    # Get recipes first to have a valid recipe_id
    response = requests.get(f"{API_BASE}/recipes")
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            recipe_id = recipes[0]['id']
            
            # Test start recipe command
            command_data = {
                "command": "start_recipe",
                "parameters": {
                    "recipe_id": recipe_id
                }
            }
            
            response = requests.post(
                f"{API_BASE}/device/commands",
                json=command_data,
                headers={'Content-Type': 'application/json'}
            )
            print_response(response, "Start Recipe Command")
    
    # Test reset command
    command_data = {
        "command": "reset",
        "parameters": {}
    }
    
    response = requests.post(
        f"{API_BASE}/device/commands",
        json=command_data,
        headers={'Content-Type': 'application/json'}
    )
    print_response(response, "Reset Command")

def main():
    """Run all tests"""
    print("🚀 Manufacturing REST API Test Suite")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        test_demo_endpoint()
        test_api_documentation()
        
        # Test data retrieval
        test_contacts_api()
        test_wires_api()
        test_processes_api()
        test_recipes_api()
        
        # Test CRUD operations
        test_create_and_delete()
        
        # Test device commands
        test_device_commands()
        
        print("\n✅ All tests completed!")
        print("\n📖 API Documentation available at:")
        print(f"   {BASE_URL}/api/v1/docs")
        print(f"\n🎯 Demo endpoint available at:")
        print(f"   {BASE_URL}/api/demo")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("   Make sure the server is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 