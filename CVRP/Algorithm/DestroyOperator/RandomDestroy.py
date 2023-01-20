from random import randint
from CVRP.Instances.Route import erase
from numba import njit


@njit(cache=True)
def random_destroy_v2(to_remove, solution, route_length, route_costs, route_load, demand, distance_matrix, removes):
    """
    Hàm này thực hiện xóa ngẫu nhiên khách hàng từ 1 route bất kì
    """
    removed = 0
    while removed < to_remove:
        random_route = randint(0, len(solution) - 1)
        # Neu route co customer ngoai depot ra
        if route_length[random_route] > 2:
            # Chon ngau nhien 1 vi tri de xoa ma khong phai depot
            random_position = randint(1, route_length[random_route] - 2)
            # update mang remove dua tren ID bi xoa
            removes[removed] = solution[random_route][random_position]
            # Xoa dua tren vi tri random
            erase(random_position, random_route, solution, route_length, route_costs, route_load, demand, distance_matrix)
            removed += 1
