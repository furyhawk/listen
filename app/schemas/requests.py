from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str


class PetCreateRequest(BaseRequest):
    pet_name: str


class MqttCreateRequest(BaseRequest):
    publish_received_at: int
    pub_props: dict
    peerhost: str
    qos: int
    topic: str
    clientid: str
    payload: str
    username: str
    event: str
    metadata: dict
    timestamp: int
    node: str
    id: str
    flags: dict


# {
#     "publish_received_at": 1714785223633,
#     "pub_props": {"User-Property": {}},
#     "peerhost": "192.168.50.1",
#     "qos": 0,
#     "topic": "temperature",
#     "clientid": "e661a4d4177d8a2a",
#     "payload": "27.51C",
#     "username": "user1",
#     "event": "message.publish",
#     "metadata": {"rule_id": "sink_WH_D"},
#     "timestamp": 1714785223633,
#     "node": "emqx@node1.emqx.io",
#     "id": "000617968C1EEAD9DB5B00000CFD0E24",
#     "flags": {"retain": false, "dup": false},
# }
