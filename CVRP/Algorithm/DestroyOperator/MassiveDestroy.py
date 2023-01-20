import numpy as np
from numba import njit


@njit(cache=True)
def massive_destroy_v2(solution, route_length, route_costs, route_load, removed):
    """
    Ham nay thuc hien xoa tat ca khach hang tu 2 route ngau nhien
    """
    target = np.random.choice(np.arange(len(solution)), 2, replace=False)
    it = 0
    for i in range(1, route_length[target[0]] - 1):
        removed[it] = solution[target[0]][i]
        solution[target[0]][i] = 0
        it += 1

    for i in range(1, route_length[target[1]] - 1):
        removed[it] = solution[target[1]][i]
        solution[target[1]][i] = 0
        it += 1

    route_costs[target[0]] = 0
    route_costs[target[1]] = 0
    route_load[target[0]] = 0
    route_load[target[1]] = 0
    route_length[target[0]] = 2
    route_length[target[1]] = 2
