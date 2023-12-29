from typing import List
from enum import Enum
from typing import Dict

MSG_PICKUP_RESPONSE = "pickup_response"
MSG_PICKUP_REQUEST = "pickup_request"
MSG_DELIVERY_NOTIFY = "delivery_notify"

class Message:
    def __init__(self, type: str, sender_id: str, destination_id: str, value: Dict) -> None:
        self.sender_id = sender_id
        self.destination_id = destination_id
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"Message {self.sender_id} -> {self.destination_id} of type {self.type}. Contents: {self.value}"


class CommunicationLayer:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls, agents=[], broker=None):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.agents = agents
            cls.broker = broker
        return cls._instance

    @classmethod
    def send_to_broker(cls, message: Message):
        cls.broker.receive_message(message)

    @classmethod
    def send_to_agent(cls, agent_id, message: Message):
        for agent in cls.agents:
            if agent.id == agent_id:
                agent.receive_message(message)
                break
        else:
            raise RuntimeError(f"No destination agent with id {message.destination_id} found")

    def get_all_agent_destinations(cls):
        return cls.agents

    # notify all agents in our grid. (When broker sends messages to all agents)
    @classmethod
    def notify_agents(cls, message):
        for agent in cls.agents:
            agent.receive_message(message)

    # returns a list of all agent destinations
    @classmethod
    def all_agent_destinations(cls):
        return cls.agents


