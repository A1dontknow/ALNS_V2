from CVRP.Instances.Route import erase
from numba import njit


@njit(cache=True)
def find_worst_position_v2(solution, route_length, distance_matrix):
    worst = 0
    a = b = -1
    for i in range(len(solution)):
        # Ko xet 2 cai depot
        for j in range(1, route_length[i] - 1):
            current = solution[i][j]
            before = solution[i][j-1]
            after = solution[i][j+1]
            cost = distance_matrix[before][current] + distance_matrix[current][after] - distance_matrix[before][after]
            if cost > worst:
                a, b = i, j
    return a, b


@njit(cache=True)
def worst_destroy_v2(to_remove, solution, route_length, route_costs, route_load, demand, distance_matrix, removed):
    """
    Ham nay se loai bo nhung khach hang nao làm cho hàm chi phí giảm nhiều nhất
    """
    it = 0
    while it < to_remove:
        # Tìm vị trí được cho là làm hàm chi phí giảm nhiều nhất
        i, j = find_worst_position_v2(solution, route_length, distance_matrix)
        removed[it] = solution[i][j]
        erase(j, i, solution, route_length, route_costs, route_load, demand, distance_matrix)
        it += 1
