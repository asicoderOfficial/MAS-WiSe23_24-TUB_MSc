from collections import defaultdict
from src.environment.communication.communication_layer import MSG_BID_ACCEPT, MSG_BID_REJECT, MSG_DELIVERY_ANNOUNCE, MSG_PLACE_BID, CommunicationLayer, Message

class KitchenInitiator:
    def __init__(self, broker_id) -> None:
        self.id = broker_id
        self.current_bids = defaultdict(defaultdict)  
        self.packages = {}
        
    def step(self):
        finished_bidding = []
        for package_id, package in self.packages.items():
            if len(self.current_bids[package.id]) == 0:
                self.announce_order(package)
            else:
                success = self.send_bid_response(package)
                if success:
                    finished_bidding.append(package)
        
        for package in finished_bidding:
            del self.packages[package.id]
            del self.current_bids[package.id]
        
    def add_package(self, package):
        self.packages[package.id] = package

    def announce_order(self, package):
        print(f"KitchenInitiator: Announcing order {package}")
        agent_ids = CommunicationLayer.get_all_agent_ids() 
        for agent_id in agent_ids:
            message = Message(MSG_DELIVERY_ANNOUNCE, self.id, agent_id, {"package": package})
            response = CommunicationLayer.send_to_agent(agent_id, message)
            if response.type == MSG_PLACE_BID:
                if response.value["response"] == "yes":
                    self.current_bids[package.id][agent_id] = response.value["bid"]
                    print(f"Agent {agent_id} accepted the bid with bid {response.value['bid']}.")
                else:
                    print(f"Agent {agent_id} rejected the bid.")
    
    def send_bid_response(self, package):
        best_agent = self.choose_agent(package)
        if best_agent is not None:
            message = Message(MSG_BID_ACCEPT, self.id, best_agent, {"package": package})
            CommunicationLayer.send_to_agent(best_agent, message)
            
            agent_ids = CommunicationLayer.get_all_agent_ids() 
            for agent_id in agent_ids:
                if agent_id != best_agent:
                    message = Message(MSG_BID_REJECT, self.id, agent_id, {"package": package})
                    CommunicationLayer.send_to_agent(agent_id, message)
            return True
        else:
            print(f"No agents accepted the order {package}.")
            return False
            
    def choose_agent(self, package):
        for package_id, package_bids in self.current_bids.items():
            if len(package_bids) > 0:
                best_agent = max(package_bids, key=lambda k: package_bids[k])
                print(f"Best agent for order {package} is {best_agent} with bid {package_bids[best_agent]}.")
                return best_agent
            else:
                print(f"No agents accepted the order {package}.")
                return None