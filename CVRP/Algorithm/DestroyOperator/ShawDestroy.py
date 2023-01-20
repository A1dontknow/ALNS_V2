from random import randint, random
from numba import njit
from CVRP.Instances.Route import erase_id
import numpy as np


@njit(cache=True)
def get_in_plan_v2(to_remove, route_length):
    i = randint(0, len(route_length) - 1)
    while route_length[i] < to_remove + 2:
        i = randint(0, len(route_length) - 1)
    return i



@njit(cache=True)
def rank_using_relatedness_v2(v, it, visit_sets, distance_matrix):
    relate = np.full(len(visit_sets), 99999, dtype=np.int32)

    for i in range(it + 1, len(visit_sets) - 1):
        relate[i] = distance_matrix[v][visit_sets[i]]

    # Tra ve ranking theo index, not ID
    s = relate.argsort()
    return s


@njit(cache=True)
def shaw_destroy_v2(to_remove, solution, d, route_length, route_costs, route_load, demand, distance_matrix, removed):
    """
    Ham nay duoc implement tu bai bao Shaw P. Using constraint programming and local search
    methods to vehicle routing problem. Lecture Notes in Computer Science 1998;1520:417–30
    """

    # Chọn 1 tuyến thích hợp để destroy
    selected_route = get_in_plan_v2(to_remove, route_length)
    # visit_sets chép những khách hàng nằm trong route được chọn để xóa
    visit_sets = np.copy(solution[selected_route][0:route_length[selected_route]])
    r = randint(1, len(visit_sets) - 2)

    # Mảng removed sẽ lưu thông tin những ID sẽ xóa
    removed[0] = visit_sets[r]
    # Lazy delete (giảm độ phức tạp của operator nhưng tăng độ khó khi implement)
    visit_sets[1], visit_sets[r] = visit_sets[r], visit_sets[1]

    it = 1
    while it < to_remove:
        v = removed[randint(0, it - 1)]
        # Rank visits in plan with respect to relatedness to v. Rank will be increasing order
        lst = rank_using_relatedness_v2(v, it, visit_sets, distance_matrix)
        rand = random()
        # idx lấy ra vị trứ chứa ID cần xóa. trừ đi it vì fake delete, trừ 2 cho 2 depot
        idx = lst[int((len(lst) - 1 - it - 2) * rand ** d)]
        removed[it] = visit_sets[idx]
        # Lazy delete
        visit_sets[it + 1], visit_sets[idx] = visit_sets[idx], visit_sets[it + 1]
        it += 1

    # Tiến hành xóa trong solution
    for i in range(it):
        erase_id(removed[i], selected_route, solution, route_length, route_costs, route_load, demand, distance_matrix)