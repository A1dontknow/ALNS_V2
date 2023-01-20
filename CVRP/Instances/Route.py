from numba import njit


@njit(cache=True)
def can_insert(node_id, route_id, route_load, demand, capacity):
    """
    Hàm kiểm tra việc chèn vào route có khả thi hay không
    """
    return route_load[route_id] + demand[node_id] <= capacity


@njit(cache=True)
def erase(position, route_id, solution, route_length, route_costs, route_load, demand, distance_matrix):
    """
    Hàm thực hiện xóa khách hàng có vị trí là position từ tuyến route_id trong nghiệm
    Chi phí, tải trọng và số lượng khách trong tuyến sẽ được cập nhật sau khi xóa
    """
    prev = solution[route_id][position - 1]
    removing = solution[route_id][position]
    after = solution[route_id][position + 1]
    route_costs[route_id] += distance_matrix[prev][after] - distance_matrix[prev][removing] - distance_matrix[removing][after]
    route_load[route_id] -= demand[removing]
    route_length[route_id] -= 1
    while solution[route_id][position] != 0:
        solution[route_id][position] = solution[route_id][position + 1]
        position += 1


@njit(cache=True)
def erase_id(node_id, route_id, solution, route_length, route_costs, route_load, demand, distance_matrix):
    """
    Hàm thực hiện xóa khách hàng có ID là node_id từ tuyến route_id trong nghiệm
    Chi phí, tải trọng và số lượng khách trong tuyến sẽ được cập nhật sau khi xóa
    """
    for i in range(route_length[route_id]):
        if solution[route_id][i] == node_id:
            erase(i, route_id, solution, route_length, route_costs, route_load, demand, distance_matrix)
            break

@njit(cache=True)
def insert(node_id, position, route_id, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix):
    """
    Hàm thực hiện chèn khách hàng có ID là node_id từ tuyến route_id trong nghiệm
    Chi phí, tải trọng và số lượng khách trong tuyến sẽ được cập nhật sau khi chèn
    """
    if can_insert(node_id, route_id, route_load, demand, capacity):
        route_length[route_id] += 1
        route_load[route_id] += demand[node_id]
        prev = solution[route_id][position]
        after = solution[route_id][position + 1]
        route_costs[route_id] += distance_matrix[prev][node_id] + distance_matrix[node_id][after] - distance_matrix[prev][after]
        for i in range(route_length[route_id], position + 1, -1):
            solution[route_id][i] = solution[route_id][i-1]
        solution[route_id][position + 1] = node_id