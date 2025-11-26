import requests
import msgpack
import json

API_URL = "http://127.0.0.1:8001/api/data/" 
TEST_DATA = {'name': 'Roronoa Zoro', 'age': 25, 'description': 'Roronoa Zoro is the combatant of the Straw Hat Pirates and one of the most iconic characters in One Piece. Physically imposing and incredibly muscular, Zoro stands tall with a powerful, broad-shouldered frame that reflects his years of relentless training and countless life-or-death battles. His appearance is instantly recognizable: short green hair, sharp eyes often narrowed in focus, and a stern expression that makes him look perpetually serious—even when he’s asleep or hopelessly lost. A defining part of his look is the black bandana tied around his left bicep, which he only wears on his head during the toughest battles, signaling that he’s fighting at full strength. Zoro wields three swords in a unique style known as Santoryu—the Three-Sword Style—where he holds one sword in each hand and a third in his mouth. His treasured blade is Wado Ichimonji, a white sword with deep personal significance tied to his childhood friend Kuina. Over the course of the series, he acquires other legendary swords such as the cursed Sandai Kitetsu, the black blade Shusui (later replaced with Enma), and his swordsmanship grows so powerful that entire buildings, ships, and mountains fall before his techniques. His body is a map of scars, each marking a brutal confrontation. The most famous is the massive X-shaped scar across his torso, inflicted by Mihawk during their first duel—a wound that represents both Zoro’s greatest defeat and the moment that hardened his resolve to surpass all limits. Another is the scar that runs over his left eye, earned during training with Mihawk during the two-year timeskip; though its origin is still mysterious, fans associate it with power he has yet to fully reveal. Personality-wise, Zoro is stern, disciplined, and unwavering in his convictions. He projects an aura of quiet intensity and rarely allows emotions to cloud his judgment. Though he is often blunt or harsh in his words, his loyalty to Luffy and the crew runs deeper than anything else. Zoro is the type who will throw himself in front of death without hesitation if it means protecting his captain’s dream. One of his most defining moments is when he takes on all of Luffy pain'}

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