from src.agents.perception import Perception
from src.environment.communication.CommunicationChainAgent import CommunicationChainAgent
from src.environment.communication.broker import Broker
from src.environment.communication.communication_layer import CommunicationLayer, Message
from src.environment.package_point import PACKAGE_POINT_INTERMEDIATE

from src.utils.position import Position

def first_test():
    #agent1 = Agent("1", Position(0,0), [], Perception(1), "dijkstra")
    #agent2 = Agent("2", Position(1,1), [], Perception(1), "dijkstra")
    broker = Broker()

    comm_layer = CommunicationLayer.instance([agent1, agent2], broker)

    message = Message("None", agent1.id, "broker", {"value": 1})
    agent1.send_broker_message(message)

    message = Message("None", "broker", agent1.id, {"value": 2})
    broker.send_message(message)

    message = Message("None", agent1.id, agent2.id, {"value": 3})
    agent1.send_agent_message(message)


# Define constants
PACKAGE_POINT_INTERMEDIATE = "IP-1"

agent1 = CommunicationChainAgent(id="1", position=Position(0, 0), package=[], perception=Perception(1), algorithm_name="dijkstra", goal_package_point=PACKAGE_POINT_INTERMEDIATE)
#agent2 = CommunicationChainAgent("2", Position(1, 1), [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra")


broker = Broker(broker_id="broker1")

# Initialize CommunicationLayer between agent and broker
comm_layer = CommunicationLayer.instance([agent1], broker)

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

print ("TEST 3")
# Test: Agent1 sends a pickup request to the broker
package_id = "123"
intermediate_point = "A"
broker.send_pickup_request(agent1.id, package_id, intermediate_point)

# Test: Broker receives a pickup response from Agent1
pickup_response_message = Message("pickup_response", agent1.id, broker.id, {"response": "yes"})
broker.receive_message(pickup_response_message)

print(f"Agent ID: {agent1.id}")
print(f"Agent Position: {agent1.pos}")
print(f"Agent Goal Package Point: {agent1.goal_package_point}")
print(f"Agent Algorithm: {agent1.algorithm_name}")