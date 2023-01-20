import numpy as np
from numba import njit


@njit(cache=True)
def get_initial_solution(vehicles, capacity, demand, distance_matrix):
    """
    :param vehicles: So luong xe
    :param capacity: Trong tai toi da moi xe
    :param demand: Nhu cau tung khach hang
    :param distance_matrix: Ma tran khoang cach
    :return solution: Nghiệm ban đầu
    :return route_length: Số lượng khách hàng trên từng Route. Do mảng bị fix cứng nên cần kiểm soát điều này
    :return route_costs: Chi phí của từng tuyến
    :return route_load: Tải trọng hiện tại của mỗi xe

    Ham nay dung nghiem ban dau cho bai toan bằng Nearest Neighbor Heuristic
    """
    solution = np.zeros((vehicles, len(demand)), dtype=np.int32)
    route_length = np.zeros(vehicles, dtype=np.int32)
    allocated = np.zeros(len(demand))
    route_costs = np.zeros(vehicles)
    route_load = np.zeros(vehicles)
    closet_node = 0
    current_route = 0
    inserted = 0
    it = 0

    # Allocate tung customer den tung route
    while inserted != len(demand) - 1:
        min_distance = 99999
        # Di tim khach hang (tru kho) co khoang cach gan nhat
        for j in range(1, len(demand)):
            # Neu van co the insert duoc va chua duoc allocate
            if route_load[current_route] + demand[j] <= capacity and allocated[j] == 0:
                if distance_matrix[solution[current_route][it]][j] < min_distance:
                    min_distance = distance_matrix[solution[current_route][it]][j]
                    closet_node = j

        # Insert khach hang gan nhat vao route (theo cach encode solution)
        if min_distance != 99999:
            inserted += 1
            allocated[closet_node] = 1
            route_costs[current_route] += min_distance
            route_load[current_route] += demand[closet_node]
            solution[current_route][it + 1] = closet_node
            it += 1
        # Truong hop neu khong tim duoc customer de chen thi tao route moi
        else:
            # tinh toan cost khi quay ve depot
            route_costs[current_route] += distance_matrix[closet_node][0]
            route_length[current_route] = it + 2
            current_route += 1
            it = 0

        if inserted == len(demand) - 1:
            route_costs[current_route] += distance_matrix[closet_node][0]
            route_length[current_route] = it + 2

    return solution, route_length, route_costs, route_load
