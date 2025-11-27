import msgpack
from locust import User, task, between
import httpx

TEST_DATA = {
    'name': 'Roronoa Zoro',
    'age': 25,
    'description': 'Roronoa Zoro is the combatant of the Straw Hat Pirates and one of the most iconic characters in One Piece. Physically imposing and incredibly muscular, Zoro stands tall with a powerful, broad-shouldered frame that reflects his years of relentless training and countless life-or-death battles. His appearance is instantly recognizable: short green hair, sharp eyes often narrowed in focus, and a stern expression that makes him look perpetually serious—even when he’s asleep or hopelessly lost. A defining part of his look is the black bandana tied around his left bicep, which he only wears on his head during the toughest battles, signaling that he’s fighting at full strength. Zoro wields three swords in a unique style known as Santoryu—the Three-Sword Style—where he holds one sword in each hand and a third in his mouth. His treasured blade is Wado Ichimonji, a white sword with deep personal significance tied to his childhood friend Kuina. Over the course of the series, he acquires other legendary swords such as the cursed Sandai Kitetsu, the black blade Shusui (later replaced with Enma), and his swordsmanship grows so powerful that entire buildings, ships, and mountains fall before his techniques. His body is a map of scars, each marking a brutal confrontation. The most famous is the massive X-shaped scar across his torso, inflicted by Mihawk during their first duel—a wound that represents both Zoro’s greatest defeat and the moment that hardened his resolve to surpass all limits. Another is the scar that runs over his left eye, earned during training with Mihawk during the two-year timeskip; though its origin is still mysterious, fans associate it with power he has yet to fully reveal. Personality-wise, Zoro is stern, disciplined, and unwavering in his convictions. He projects an aura of quiet intensity and rarely allows emotions to cloud his judgment. Though he is often blunt or harsh in his words, his loyalty to Luffy and the crew runs deeper than anything else. Zoro is the type who will throw himself in front of death without hesitation if it means protecting his captain’s dream. One of his most defining moments is when he takes on all of Luffy pain'
}

PACKED_DATA = msgpack.packb(TEST_DATA)

class ApiUser(User):
    wait_time = between(1, 2.5)
    host = "http://127.0.0.1:8001"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http2_client = httpx.Client(base_url=self.host, http2=True, timeout=10.0)

    @task
    def post_msgpack(self):
        headers = {
            'Content-Type': 'application/msgpack',
            'Accept': 'application/msgpack',
        }

        name = "POST /api/data/ (MsgPack)"

        try:
            response = self.http2_client.post("/api/data/", content=PACKED_DATA, headers=headers)
            response_time_ms = response.elapsed.total_seconds() * 1000

            if response.status_code == 200:
                content = msgpack.unpackb(response.content, raw=False)
                if content.get('name') == TEST_DATA['name'] and content.get('age') == TEST_DATA['age']:
                    self.environment.events.request.fire(
                        request_type="POST",
                        name=name,
                        response_time=response_time_ms,
                        response_length=len(response.content),
                        exception=None
                    )
                else:
                    self.environment.events.request.fire(
                        request_type="POST",
                        name=name,
                        response_time=response_time_ms,
                        response_length=len(response.content),
                        exception=Exception("Response data mismatch")
                    )
            else:
                self.environment.events.request.fire(
                    request_type="POST",
                    name=name,
                    response_time=response_time_ms,
                    response_length=len(response.content),
                    exception=Exception(f"Status code {response.status_code}")
                )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="POST",
                name=name,
                response_time=0,
                response_length=0,
                exception=e
            )
