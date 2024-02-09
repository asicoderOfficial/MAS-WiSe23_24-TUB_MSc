from typing import List
from enum import Enum
from typing import Dict

from src.visualization.save import Save

# Broker
MSG_PICKUP_RESPONSE = "pickup_response"
MSG_PICKUP_REQUEST = "pickup_request"
MSG_DELIVERY_NOTIFY = "delivery_notify"
MSG_DELIVERY_ACCEPTED = "delivery_accepted"
MSG_PACKAGE_DELIVERED = "package_delivered"

# Contract Network Protocol
MSG_DELIVERY_ANNOUNCE = "delivery_announce"
MSG_PLACE_BID = "place_bid"
MSG_BID_ACCEPT = "bid_accept"
MSG_BID_REJECT = "bid_reject"

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
            cls.init(agents, broker)
        return cls._instance
    
    @classmethod
    def init(cls, agents=[], broker=None):
        cls._instance = cls.__new__(cls)
        cls.agents = agents
        cls.broker = broker

    @classmethod
    def send_to_broker(cls, message: Message):
        Save.save_to_csv_messages(message, "Message to broker:")
        cls.broker.receive_message(message)

    @classmethod
    def send_to_agent(cls, agent_id, message: Message):
        for agent in cls.agents:
            if agent.id == agent_id:
                Save.save_to_csv_messages(message, "Message to agent:")
                return agent.receive_message(message)
        else:
            raise RuntimeError(f"No destination agent with id {message.destination_id} found")

    def get_all_agent_ids(cls):
        return cls.agents

    # returns a list of all agent destinations
    @classmethod
    def get_all_agent_ids(cls):
        return [agent.id for agent in cls.agents]
