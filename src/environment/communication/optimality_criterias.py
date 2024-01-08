from src.environment.communication.communication_layer import MSG_DELIVERY_ACCEPTED, MSG_DELIVERY_NOTIFY, MSG_PICKUP_REQUEST, CommunicationLayer, Message
from src.utils.position import Position



def naive(initiating_agent_id:str, target_package_id:str, target_package_pos:Position):
    agents_ids = CommunicationLayer.get_all_agent_ids()
    for agent_id in agents_ids:
        if agent_id != initiating_agent_id:
            message = Message(MSG_PICKUP_REQUEST, "broker", agent_id, {
                "pos": target_package_pos, 
                "package_id": target_package_id,
            }
            )
            response = CommunicationLayer.send_to_agent(agent_id, message)
            if response is not None and response.value["response"] == "yes":
                return agent_id
