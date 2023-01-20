from CVRP.Instances.Route import insert, can_insert
from numba import njit


@njit
def find_best_position_v2(node, solution, route_length, route_load, demand, capacity, distance_matrix):
    min_cost = 999999
    a, b = -1, -1

    for i in range(len(solution)):
        if can_insert(node, i, route_load, demand, capacity):
            for j in range(route_length[i] - 1):
                before = solution[i][j]
                after = solution[i][j+1]
                cost = distance_matrix[before][node] + distance_matrix[node][after] - distance_matrix[before][after]

                if cost < min_cost:
                    min_cost = cost
                    a, b = i, j

    return a, b


@njit
def greedy_repair_v2(removed, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix):
    """
    Hàm này sửa nghiệm nào làm cho hàm chi phí tăng ít nhất
    """
    it = 0
    while removed[it] != 0:
        # Tìm vị trí thích hợp để sửa sao cho hàm chi phí tăng ít nhất
        a, b = find_best_position_v2(removed[it], solution, route_length, route_load, demand, capacity, distance_matrix)
        # Xét trường hợp nếu không thể sửa được nghiệm do capacity constraint
        if a == -1 or b == -1:
            return False
        insert(removed[it], b, a, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
        removed[it] = 0
        it += 1
    return True
