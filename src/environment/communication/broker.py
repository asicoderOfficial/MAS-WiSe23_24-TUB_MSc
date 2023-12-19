from typing import List
from src.environment.communication.communication_layer import CommunicationLayer, Message


class Broker:    
    def send_message(self, message: Message):
        print("Broker: Sending message to an agent", message.destination_id)
        CommunicationLayer.send_to_agent(message)
    
    def receive_message(self, message: Message):
        """Pass a message to the broker

        Args:
            message (Message): The message to pass to the broker
        """
        print("Received message:", message)
        # TODO: logic
    
    