from src.agents.perception import Perception
from src.environment.communication.broker import Broker
from src.environment.communication.communication_layer import CommunicationLayer, Message
from src.agents.agent import Agent
from src.utils.position import Position


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