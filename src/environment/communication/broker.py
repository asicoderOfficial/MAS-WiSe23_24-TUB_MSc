from typing import List
from src.environment.communication.communication_layer import MSG_DELIVERY_NOTIFY, MSG_PICKUP_REQUEST, CommunicationLayer, Message
from src.utils.position import Position


class Broker:
    def __init__(self, broker_id):
        self.id = broker_id
        self.waiting_packages = []
        
    def step(self):
        for package in self.waiting_packages:
            self.find_delivery_agent(package["package_id"], package["pos"])
    
    def send_message(self,  message: Message):
        print("Broker: Sending message to an agent", message.destination_id)
        CommunicationLayer.send_to_agent(message.destination_id, message)

    def send_pickup_request(self, agent_id, package_id, intermediate_point):
        message = Message(MSG_PICKUP_REQUEST, self.id, agent_id, {"package_id": package_id, "intermediate_point": intermediate_point})
        CommunicationLayer.send_to_agent(agent_id, message)

    # logic for receiving information when agent will take parcel
    def receive_message(self, message: Message):
        """Pass a message to the broker
        Args:
            message (Message): The message to pass to the broker
        """
        
        print(f"Broker received message: {message}")
        if message.type == MSG_DELIVERY_NOTIFY:
            self.find_delivery_agent(message.value["package_id"], message.value["pos"], new=True)            

    def find_delivery_agent(self, package_id: str, package_pos: Position, new: bool = False):
        """Find an agent that accepts task to delivery the package

        Args:
            package_id (str): package id
            package_pos (Position): package position
            new (bool, optional): whether package was just received (and is not in waiting list). Defaults to False.
        """
        agents_ids = CommunicationLayer.get_all_agent_ids()
        for agent_id in agents_ids:
            message = Message(MSG_PICKUP_REQUEST, "broker", agent_id, {
                "pos": package_pos, 
                "package_id": package_id
            })
            response = CommunicationLayer.send_to_agent(agent_id, message)
            if response is not None and response.value["response"] == "yes":
                print(f"Agent {agent_id} accepted the pickup request. Assigning task...")
                break
        else:
            print(f"No agent found to pick up package {package_id}. will repeat in the next step")
            if new:
                self.waiting_packages.append({
                    "package_id": message.value["package_id"], 
                    "pos": message.value["pos"],
                })