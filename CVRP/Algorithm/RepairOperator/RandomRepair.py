from random import randint
import numpy as np
from CVRP.Instances.Route import insert, can_insert
from numba import njit


@njit
def random_repair_v2(removed, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix):
    """
    Hàm này sửa ngẫu nhiên khách hàng vào vị trí ngẫu nhiên. Ko có quy tắc gì cả
    """

    it = it2 = 0

    while removed[it] != 0:
        # Liệt kê các route có thể chèn vào được
        insert_route = np.zeros(len(solution), dtype=np.int32)
        for i in range(len(solution)):
            if can_insert(removed[it], i, route_load, demand, capacity):
                insert_route[it2] = i
                it2 += 1

        # Nếu không tồn tại route nào -> nghiệm không sửa được -> Trả về False để xử lý
        if it2 == 0:
            return False

        route_id = insert_route[randint(0, it2 - 1)]
        position = randint(0, route_length[route_id] - 2)
        insert(removed[it], position, route_id, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
        removed[it] = 0
        it += 1
        it2 = 0

    return True
