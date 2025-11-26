import requests
import msgpack
import json

API_URL = "http://127.0.0.1:8000/api/data/" 
TEST_DATA = {'name': 'Khanh Super', 'age': 25}

# --- Test Case 1: Send MsgPack, Expect MsgPack (High Performance) ---

packed_data = msgpack.packb(TEST_DATA)

headers_msgpack = {
    'Content-Type': 'application/msgpack',
    'Accept': 'application/msgpack',
}

print("Testing: MsgPack Input / MsgPack Output")
response = requests.post(API_URL, data=packed_data, headers=headers_msgpack)

if response.status_code == 200:
    unpacked_data = msgpack.unpackb(response.content, raw=False)
    print("  Success! Response Data (Unpacked):", unpacked_data)
else:
    print(f"  Error {response.status_code}: {response.text}")


# --- Test Case 2: Send JSON, Expect JSON (Standard) ---

json_data = json.dumps(TEST_DATA)

headers_json = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

print("\nTesting: JSON Input / JSON Output")
response = requests.post(API_URL, data=json_data, headers=headers_json)

if response.status_code == 200:
    print("  Success! Response Data (JSON):", response.json())
else:
    print(f"  Error {response.status_code}: {response.text}")