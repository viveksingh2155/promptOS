import socket
import requests
import os
import subprocess

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_ollama():
    try:
        response = requests.get('http://127.0.0.1:11434/api/tags')
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            return True, models
        return False, f"Status code: {response.status_code}"
    except Exception as e:
        return False, str(e)

def run_diagnostics():
    print("--- PromptOS Systems Diagnostics ---")
    
    # 1. Ollama
    print("[1/4] Checking Ollama service...")
    ok, result = check_ollama()
    if ok:
        print(f"  ✅ Ollama is running. Available models: {result}")
        if 'llama3.1:latest' in result or 'llama3.1' in result:
             print("  ✅ llama3.1 is available.")
        else:
             print("  ❌ llama3.1 is NOT available. Please pull it.")
        if 'phi3.5:latest' in result or 'phi3.5' in result:
             print("  ✅ phi3.5 is available.")
        else:
             print("  ❌ phi3.5 is NOT available.")
    else:
        print(f"  ❌ Ollama check failed: {result}")

    # 2. Ports
    print("[2/4] Checking ports...")
    for port in [3000, 3001, 8000]:
        if check_port(port):
            print(f"  ⚠️ Port {port} is IN USE. This might cause issues.")
        else:
            print(f"  ✅ Port {port} is free.")

    # 3. Backend Env
    print("[3/4] Checking backend virtual environment...")
    venv_path = "backend/venv/bin/python"
    if os.path.exists(venv_path):
        print("  ✅ Backend venv found.")
    else:
        print("  ❌ Backend venv NOT found.")

    # 4. Frontend Env
    print("[4/4] Checking frontend node_modules...")
    if os.path.exists("frontend/node_modules"):
        print("  ✅ Frontend node_modules found.")
    else:
        print("  ❌ Frontend node_modules NOT found.")

if __name__ == "__main__":
    run_diagnostics()
