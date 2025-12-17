from django.test import TestCase

# Create your tests here.
import requests

BASE_URL = "http://127.0.0.1:8000"

print("="*60)
print("CREATING AND TESTING DUMMY USER")
print("="*60)

# Step 1: Register dummy user
print("\n1. Registering dummy user...")
register_data = {
    "email": "dummy@example.com",
    "first_name": "Dummy",
    "last_name": "User",
    "password": "dummypass123",
    "password2": "dummypass123"
}

response = requests.post(f"{BASE_URL}/api/auth/register/", json=register_data)
print(f"Status: {response.status_code}")
if response.status_code == 201:
    print("✓ Dummy user created!")
    print(response.json())
else:
    print("User might already exist, continuing to login...")

# Step 2: Login with dummy user
print("\n2. Logging in as dummy user...")
login_data = {
    "email": "dummy@example.com",
    "password": "dummypass123"
}

response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
tokens = response.json()
print(f"Status: {response.status_code}")
print(f"✓ Got access token: {tokens['access'][:50]}...")

# Step 3: Get dummy user's profile
print("\n3. Getting dummy user's profile...")
headers = {"Authorization": f"Bearer {tokens['access']}"}
response = requests.get(f"{BASE_URL}/api/auth/profile/", headers=headers)

print(f"Status: {response.status_code}")
print("\n✓ DUMMY USER'S PROFILE:")
print("="*60)
import json
print(json.dumps(response.json(), indent=2))
print("="*60)