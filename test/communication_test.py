from src.agents.perception import Perception
from src.agents.strategies.communication_chain_agent import CommunicationChainAgent
from src.environment.communication.broker import Broker
from src.environment.communication.communication_layer import MSG_DELIVERY_NOTIFY, MSG_PICKUP_REQUEST, MSG_PICKUP_RESPONSE, MSG_DELIVERY_ACCEPTED, CommunicationLayer, Message
from src.environment.package_point import PACKAGE_POINT_INTERMEDIATE

from src.utils.position import Position


# Define constants
PACKAGE_POINT_INTERMEDIATE = "IP-1"
package_id = "123"
intermediate_point = "A"
intermediate_point_pos = (5,5)

agent1 = CommunicationChainAgent(id="1", position=Position(0, 0), packages=[], perception=Perception(1), algorithm_name="dijkstra", goal_package_point=PACKAGE_POINT_INTERMEDIATE)
#agent2 = CommunicationChainAgent("2", Position(1, 1), [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra")
broker = Broker(broker_id="broker1")

# Initialize CommunicationLayer between agent and broker
comm_layer = CommunicationLayer.instance([agent1], broker)


print ("TEST 1")
# Test: Agent1 informs the broker about delivering a package
delivery_message = Message(MSG_DELIVERY_NOTIFY, agent1.id, "broker", {"package_id": package_id, "status": "delivered", "pos": intermediate_point_pos})

# Check if the communication layer with broker established before sending the message
if CommunicationLayer.broker:
    agent1.send_broker_message(delivery_message)
else:
    print("Error: Broker not set in CommunicationLayer")

print ("TEST 2")
# Test: Broker sends a pickup request to Agent1
message_to_agent1 = Message(MSG_PICKUP_REQUEST, "broker", agent1.id, {"package_id": package_id, "pos": intermediate_point_pos})
broker.send_message(message_to_agent1)

print ("TEST 3")
# Test: Broker receives a pickup response from Agent1
pickup_response_message = Message(MSG_PICKUP_RESPONSE, agent1.id, broker.id, {"response": "yes"})
agent1.send_broker_message(pickup_response_message)

print("TEST 4")
# Test: Broker sends the agent confirmation, to the beginner agent
message_to_agent1 = Message(MSG_DELIVERY_ACCEPTED, "broker", agent1.id, {"package_id": package_id, "pos": intermediate_point_pos})
broker.send_message(message_to_agent1)


print(f"Agent ID: {agent1.id}")
print(f"Agent Position: {agent1.pos}")
print(f"Agent Goal Package Point: {agent1.goal_package_point}")
print(f"Agent Algorithm: {agent1.algorithm_name}")