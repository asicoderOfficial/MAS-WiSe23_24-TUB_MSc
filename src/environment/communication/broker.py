from typing import List
from src.environment.communication.communication_layer import CommunicationLayer, Message


class Broker:
    def send_message(self,  message: Message):
        print("Broker: Sending message to an agent", message.destination_id)
        CommunicationLayer.send_to_agent(message.destination_id, message)

    """Pass a message to the broker

    Args:
        message (Message): The message to pass to the broker
    """
    #def receive_message(self, message: Message):
    #    print("Received message:", message)


    def send_pickup_request(self, agent_id, package_id, intermediate_point):
        message = Message("request_pickup", self.id, intermediate_point, {"package_id": package_id})
        CommunicationLayer.send_to_agent(agent_id, message)

    # logic for receiving information when agent will take parcel
    def receive_message(self, message: Message):
        print(f"Broker received message: {message}")
        if message.type == "pickup_response" and message.value["response"] == "yes":
            print(f"Agent {message.sender_id} accepted the pickup request. Assigning task...")
            # TODO: Implement task assignment logic
