from typing import List
from src.environment.communication.communication_layer import MSG_DELIVERY_ACCEPTED, MSG_DELIVERY_NOTIFY, MSG_PICKUP_REQUEST, CommunicationLayer, Message
from src.environment.communication.optimality_criterias import naive, closer_to_package, loneliest
from src.utils.position import Position


class Broker:
    def __init__(self, broker_id, optimality_criteria:str='naive'):
        self.id = broker_id
        self.optimality_criteria = optimality_criteria
        self.waiting_packages_id_pos = {}
        
    def step(self):
        for package_id, package_pos in self.waiting_packages_id_pos.copy().items():
            found_agent = self.find_delivery_agent(package_id, package_pos)
            if found_agent:
                del self.waiting_packages_id_pos[package_id]
    
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
            self.find_delivery_agent(message.value["package_id"], message.value["pos"], sender_id=message.sender_id, new=True, grid=message.value['grid'])

    def find_delivery_agent(self, package_id: str, package_pos: Position, sender_id:str='', new: bool = False, grid=None):
        """Find an agent that accepts task to delivery the package

        Args:
            package_id (str): package id
            package_pos (Position): package position
            new (bool, optional): whether package was just received (and is not in waiting list). Defaults to False.
        """
        if grid is None or self.optimality_criteria == 'naive':
            agent_id = naive(sender_id, package_id, package_pos)
        elif self.optimality_criteria == 'closer_to_package':
            agent_id = closer_to_package(grid, sender_id, package_id, package_pos)

        if agent_id is None:
            print(f"No agent found to pick up package {package_id}, will repeat in the next step with optimality criteria {self.optimality_criteria}.")
            if new:
                self.waiting_packages_id_pos[package_id] =  package_pos
            return False
        else:
            print(f"Agent {agent_id} accepted the pickup request according to optimality criteria {self.optimality_criteria}. Assigning task...")
            # Send message back to the agent that initiated the request
            message = Message(MSG_DELIVERY_ACCEPTED, "broker", sender_id, 
                {
                    "pos": package_pos, 
                    "package_id": package_id
                }
            )
            CommunicationLayer.send_to_agent(sender_id, message)

