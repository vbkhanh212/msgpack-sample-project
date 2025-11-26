import msgpack
import json
from locust import HttpUser, task, between

TEST_DATA = {
    'name': 'Roronoa Zoro',
    'age': 25,
    'description': 'Roronoa Zoro is the combatant of the Straw Hat Pirates and one of the most iconic characters in One Piece. Physically imposing and incredibly muscular, Zoro stands tall with a powerful, broad-shouldered frame that reflects his years of relentless training and countless life-or-death battles. His appearance is instantly recognizable: short green hair, sharp eyes often narrowed in focus, and a stern expression that makes him look perpetually serious—even when he’s asleep or hopelessly lost. A defining part of his look is the black bandana tied around his left bicep, which he only wears on his head during the toughest battles, signaling that he’s fighting at full strength. Zoro wields three swords in a unique style known as Santoryu—the Three-Sword Style—where he holds one sword in each hand and a third in his mouth. His treasured blade is Wado Ichimonji, a white sword with deep personal significance tied to his childhood friend Kuina. Over the course of the series, he acquires other legendary swords such as the cursed Sandai Kitetsu, the black blade Shusui (later replaced with Enma), and his swordsmanship grows so powerful that entire buildings, ships, and mountains fall before his techniques. His body is a map of scars, each marking a brutal confrontation. The most famous is the massive X-shaped scar across his torso, inflicted by Mihawk during their first duel—a wound that represents both Zoro’s greatest defeat and the moment that hardened his resolve to surpass all limits. Another is the scar that runs over his left eye, earned during training with Mihawk during the two-year timeskip; though its origin is still mysterious, fans associate it with power he has yet to fully reveal. Personality-wise, Zoro is stern, disciplined, and unwavering in his convictions. He projects an aura of quiet intensity and rarely allows emotions to cloud his judgment. Though he is often blunt or harsh in his words, his loyalty to Luffy and the crew runs deeper than anything else. Zoro is the type who will throw himself in front of death without hesitation if it means protecting his captain’s dream. One of his most defining moments is when he takes on all of Luffy pain'
}

PACKED_DATA = msgpack.packb(TEST_DATA)
JSON_DATA = json.dumps(TEST_DATA)

class ApiUser(HttpUser):
    # Time between requests in seconds (simulating user think time)
    wait_time = between(1, 2.5) 
    
    # The base URL for the API
    host = "http://127.0.0.1:8001" 

    @task() 
    def post_msgpack(self):
        # Send MsgPack, Expect MsgPack
        headers_msgpack = {
            'Content-Type': 'application/msgpack',
            'Accept': 'application/msgpack',
        }
        
        with self.client.post(
            "/api/data/", 
            data=PACKED_DATA, 
            headers=headers_msgpack, 
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    # Attempt to unpack the response content
                    msgpack.unpackb(response.content, raw=False)
                    response.success()
                except Exception as e:
                    response.failure(f"MsgPack Unpacking Failed: {e}")
            else:
                response.failure(f"Request failed with status {response.status_code}")

    # @task() 
    # def post_json(self):
    #     # Send JSON, Expect JSON
    #     headers_json = {
    #         'Content-Type': 'application/json',
    #         'Accept': 'application/json',
    #     }
        
    #     with self.client.post(
    #         "/api/data/", 
    #         data=JSON_DATA, 
    #         headers=headers_json, 
    #         catch_response=True
    #     ) as response:
    #         if response.status_code == 200:
    #             try:
    #                 # Attempt to parse the response content as JSON
    #                 response.json()
    #                 response.success()
    #             except json.JSONDecodeError as e:
    #                 response.failure(f"JSON Decoding Failed: {e}")
    #         else:
    #             response.failure(f"Request failed with status {response.status_code}")
