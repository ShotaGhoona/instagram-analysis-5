import requests
import asyncio

async def test_auth_flow():
    base_url = "http://localhost:8000"
    
    # 1. 新規ユーザー登録テスト
    register_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{base_url}/auth/register", json=register_data)
    print(f"Register response: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Registration successful. Token: {token[:20]}...")
        
        # 2. ログインテスト
        login_data = {
            "username": "testuser", 
            "password": "testpass123"
        }
        
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login response: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_token = login_response.json()["access_token"]
            print(f"Login successful. Token: {login_token[:20]}...")
        else:
            print(f"Login failed: {login_response.text}")
    else:
        print(f"Registration failed: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_auth_flow())