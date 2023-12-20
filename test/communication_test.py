from src.agents.perception import Perception
from src.environment.communication.broker import Broker
from src.environment.communication.communication_layer import CommunicationLayer, Message
from src.agents.agent import Agent
from src.utils.position import Position

def first_test():
    agent1 = Agent("1", Position(0,0), [], Perception(1), "dijkstra")
    agent2 = Agent("2", Position(1,1), [], Perception(1), "dijkstra")
    broker = Broker()

    comm_layer = CommunicationLayer.instance([agent1, agent2], broker)

    message = Message("None", agent1.id, "broker", {"value": 1})
    agent1.send_broker_message(message)

    message = Message("None", "broker", agent1.id, {"value": 2})
    broker.send_message(message)

    message = Message("None", agent1.id, agent2.id, {"value": 3})
    agent1.send_agent_message(message)



agent1 = Agent("1", Position(0, 0), [], Perception(1), "dijkstra")
agent2 = Agent("2", Position(1, 1), [], Perception(1), "dijkstra")


broker = Broker()

# Initialize CommunicationLayer between agent and broker
comm_layer = CommunicationLayer.instance([agent1, agent2], broker)

# Test: Agent1 informs the broker about delivering a package
delivery_message = Message("delivery_notification", agent1.id, "broker", {"package_id": "123", "status": "delivered"})

# Check if the communication layer with broker established before sending the message
if CommunicationLayer.broker:
    agent1.send_broker_message(delivery_message)
else:
    print("Error: Broker not set in CommunicationLayer")

print ("TEST 2")
# Test: Broker sends a message to Agent1
message_to_agent1 = Message("None", "broker", agent1.id, {"value": 2})
broker.send_message(message_to_agent1)