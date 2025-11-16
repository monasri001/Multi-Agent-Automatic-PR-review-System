"""
Check if the backend server is running
"""
import requests
import sys

def check_server():
    """Check if server is accessible"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ Backend server is running!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend server is NOT running!")
        print("\n   The server needs to be started first.")
        print("   Run this command in a terminal:")
        print("   python run_server.py")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Checking Backend Server Status")
    print("=" * 50)
    check_server()

