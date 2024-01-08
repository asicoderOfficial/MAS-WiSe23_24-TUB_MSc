import inspect

from src.environment.communication.communication_layer import MSG_PICKUP_REQUEST, CommunicationLayer, Message
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


def closer_to_package(grid, initiating_agent_id:str, target_package_id:str, target_package_pos:Position):
    agents_distances = []
    for i in range(len(grid._grid)):
        for j in range(len(grid._grid[0])):
            cell = grid._grid[i][j]
            for elem in cell:
                if 'agent' in elem.__class__.__name__.lower() and elem.id != initiating_agent_id:
                    agents_distances.append((elem.id, elem.pos.dist_to(target_package_pos)))
    
    agents_distances.sort(key=lambda x: x[1])

    for agent_id, _ in agents_distances:
        if agent_id != initiating_agent_id:
            message = Message(MSG_PICKUP_REQUEST, "broker", agent_id, {
                "pos": target_package_pos, 
                "package_id": target_package_id,
            }
            )
            response = CommunicationLayer.send_to_agent(agent_id, message)
            if response is not None and response.value["response"] == "yes":
                return agent_id


def loneliest(grid, initiating_agent_id:str, target_package_id:str, target_package_pos:Position, n_cells_around:int=4):
    agents_loneliness = []
    for i in range(len(grid._grid)):
        for j in range(len(grid._grid[0])):
            cell = grid._grid[i][j]
            for elem in cell:
                if 'agent' in elem.__class__.__name__.lower() and elem.id != initiating_agent_id:
                    curr_id = elem.id
                    agents_around = 0
                    for sub_i in range(max(0, i - n_cells_around), min(len(grid._grid), i + n_cells_around + 1)):
                        for sub_j in range(max(0, j - n_cells_around), min(len(grid._grid[0]), j + n_cells_around + 1)):
                            for sub_elem in grid._grid[sub_i][sub_j]:
                                if 'agent' in sub_elem.__class__.__name__.lower() and sub_elem.id != curr_id:
                                    agents_around += 1
                    agents_loneliness.append((curr_id, agents_around))

    agents_loneliness.sort(key=lambda x: x[1])
                    
    for agent_id, _ in agents_loneliness:
        if agent_id != initiating_agent_id:
            message = Message(MSG_PICKUP_REQUEST, "broker", agent_id, {
                "pos": target_package_pos, 
                "package_id": target_package_id,
            }
            )
            response = CommunicationLayer.send_to_agent(agent_id, message)
            if response is not None and response.value["response"] == "yes":
                return agent_id
