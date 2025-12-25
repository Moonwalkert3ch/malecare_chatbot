"""
Test script to verify usage tracking functionality.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_usage_tracking():
    print("=" * 60)
    print("Testing Usage Tracking System")
    print("=" * 60)
    
    # Test 1: Submit intake form
    print("\n1. Testing intake form submission...")
    user_id = f"test-user-{int(1000000)}"
    
    intake_data = {
        "user_id": user_id,
        "cancer_type": "Prostate Cancer",
        "stage": "Stage II",
        "age": 65,
        "sex": "Male",
        "location": "California",
        "comorbidities": ["Diabetes", "Hypertension"],
        "prior_treatments": ["Surgery", "Radiation"]
    }
    
    response = requests.post(f"{BASE_URL}/intake", json=intake_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {data.get('response', 'No response')}")
        print(f"   Trials found: {len(data.get('trials', []))}")
    else:
        print(f"   Error: {response.text}")
    
    # Test 2: Send a message
    print("\n2. Testing message tracking...")
    message_data = {
        "user_id": user_id,
        "message": "Tell me more about clinical trials near me"
    }
    
    response = requests.post(f"{BASE_URL}/message", json=message_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json().get('response', 'No response')}")
    
    # Test 3: Get admin stats
    print("\n3. Testing admin statistics endpoint...")
    response = requests.get(f"{BASE_URL}/admin/stats")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"   Total sessions: {stats['total_sessions']}")
        print(f"   Total messages: {stats['total_messages']}")
        print(f"   Cancer types: {stats['cancer_types']}")
        print(f"   Locations: {stats['locations']}")
    
    # Test 4: Test CSV export endpoint
    print("\n4. Testing CSV export endpoint...")
    response = requests.get(f"{BASE_URL}/admin/export-csv")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   CSV generated successfully")
        print(f"   Content length: {len(response.content)} bytes")
        # Show first few lines
        csv_content = response.content.decode('utf-8')
        lines = csv_content.split('\n')[:5]
        print(f"   First few lines of CSV:")
        for line in lines:
            print(f"      {line}")
    
    # Test 5: End session
    print("\n5. Testing session end tracking...")
    response = requests.post(f"{BASE_URL}/end-session", json={"user_id": user_id})
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Session ended successfully")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Visit http://localhost:3000 to test the main chatbot")
    print("2. Visit http://localhost:3000/admin to view the admin dashboard")
    print("3. Use the chatbot, then check the admin dashboard for stats")
    print("4. Download the CSV from the admin dashboard")

if __name__ == "__main__":
    try:
        test_usage_tracking()
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure the backend server is running on http://localhost:8000")
