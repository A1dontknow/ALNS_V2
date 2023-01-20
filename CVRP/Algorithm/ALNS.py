import numpy as np
import CVRP.Config as Config
from numba import njit
from CVRP.Algorithm import NearestNeighbor, LocalSearch, AdaptiveMechanism
from CVRP.Algorithm.DestroyOperator import *
from CVRP.Algorithm.RepairOperator import *

@njit(cache=True)
def solve_v2(vehicles, capacity, demand, distance_matrix):
    """
    :param vehicles: Số phương tiện
    :param capacity: Tải trọng tối đa của mỗi xe
    :param demand: Nhu cầu mỗi khách hàng
    :param distance_matrix: Ma trận biểu diễn khoảng cách từng khách hàng
    :return: Nghiệm tốt nhất tìm được và chi phí của nghiệm đó

    Ham nay giai bai toan CVRP bang thuat toan Adaptive Large Neighborhood Search. Ket qua thuat
    toan se phu thuoc vao cac tham so nam trong file /Instance/Config.py. Khi chay xong, ket qua
    se duoc luu vao /Dataset/Solution/<ten file>/
    """
    # Các biến sử dụng cho cơ chế thích nghi
    # Operator quy ước theo thứ tự: Shaw - Random - Worst - Massive (Destroy) | Greedy - Random (Repair)
    destroy_operator = np.array([0, 1, 2, 3])
    repair_operator = np.array([0, 1])

    destroy_weight = np.array([1, 1, 1, 1])
    repair_weight = np.array([1, 1])

    destroy_score = np.array([0, 0, 0, 0])
    repair_score = np.array([0, 0])

    destroy_used = np.array([0, 0, 0, 0])
    repair_used = np.array([0, 0])

    # Dựng nghiệm ban đầu
    solution, route_length, route_costs, route_load = NearestNeighbor.get_initial_solution(vehicles, capacity, demand, distance_matrix)
    # Khởi tạo nghiệm tốt nhất
    best_sol, best_cost = np.copy(solution), sum(route_costs)

    print("Ket qua sinh nghiem ban dau:")
    print(best_sol)
    test = 0
    print("ALNS Process...")

    # removed lưu trữ những khách hàng bị xóa. ips là iterate per segment
    removed = np.zeros(len(demand) - 1, dtype=np.int32)
    to_remove = int(Config.DESTROY_RATIO * (len(demand) - 1))
    ips = Config.ITERATION / Config.SEGMENT

    # Lặp thuật toán đến số lần nhất định
    for i in range(Config.ITERATION):
        # test dùng để thử nghiệm, là 1 phần của cơ chế chấp nhận nghiệm
        test += 1
        # sao chép nghiệm hiện tại để destroy/repair. Lỡ như ko repair được thì chẳng sao
        s2, r_le2, r_c2, r_lo2 = np.copy(solution), np.copy(route_length), np.copy(route_costs), np.copy(route_load)
        # Chọn cặp operator theo Roulette-wheel
        operators = AdaptiveMechanism.select_operator(destroy_operator, destroy_weight, repair_operator, repair_weight)

        # Phá nghiệm
        if operators[0] == 0:
            ShawDestroy.shaw_destroy_v2(to_remove, s2, Config.D, r_le2, r_c2, r_lo2, demand, distance_matrix, removed)
        if operators[0] == 1:
            RandomDestroy.random_destroy_v2(to_remove, s2, r_le2, r_c2, r_lo2, demand, distance_matrix, removed)
        elif operators[0] == 2:
            WorstDestroy.worst_destroy_v2(to_remove, s2, r_le2, r_c2, r_lo2, demand, distance_matrix, removed)
        elif operators[0] == 3:
            MassiveDestroy.massive_destroy_v2(s2, r_le2, r_c2, r_lo2, removed)

        # Sửa nghiệm
        can_repair = False
        if operators[1] == 0:
            can_repair = GreedyRepair.greedy_repair_v2(removed, s2, r_le2, r_c2, r_lo2, demand, capacity, distance_matrix)
        elif operators[1] == 1:
            can_repair = RandomRepair.random_repair_v2(removed, s2, r_le2, r_c2, r_lo2, demand, capacity, distance_matrix)

        # Nếu nghiệm sửa thành công thì xét các trường hợp
        if can_repair:
            s2_cost = sum(r_c2)
            # Nếu nghiệm mới tốt hơn nghiệm cũ
            if s2_cost < sum(route_costs):
                # Cải tiến cục bộ
                LocalSearch.local_search_v2(s2, r_le2, r_c2, distance_matrix)
                # Chấp nhận nghiệm mới được sinh ra
                solution, route_length, route_costs, route_load = np.copy(s2), np.copy(r_le2), np.copy(r_c2), np.copy(r_lo2)
                # Nếu nghiệm mới còn tốt hơn nghiệm tốt nhất tìm được
                if s2_cost < best_cost:
                    print(s2_cost)
                    test = 0
                    # Cập nhật nghiệm tốt nhất
                    best_sol, best_cost = np.copy(s2), s2_cost
                    # Cập nhật điểm dựa trên performance (PHI_1 > PHI_2 > PHI_3 > 0)
                    AdaptiveMechanism.update_score(operators, Config.PHI_1, destroy_score,
                                                   destroy_used, repair_score, repair_used)
                else:
                    AdaptiveMechanism.update_score(operators, Config.PHI_2, destroy_score,
                                                   destroy_used, repair_score, repair_used)
            else:
                AdaptiveMechanism.update_score(operators, Config.PHI_3, destroy_score, destroy_used,
                                               repair_score, repair_used)

            # Co che chap nhan nghiem dang duoc thu nghiem (Inspire tu thuat toan Record-to-Record)
            if s2_cost < best_cost + Config.DEVIATION:
                solution, route_length, route_costs, route_load = np.copy(s2), np.copy(r_le2), np.copy(r_c2), np.copy(r_lo2)

            # Considering very good effect (+150 for 2k total cost) (+100 for n39k6). Co time thi phat trien
            if test >= 1000 and s2_cost <= best_cost + Config.BIG_DEVIATION:
                solution, route_length, route_costs, route_load = np.copy(s2), np.copy(r_le2), np.copy(r_c2), np.copy(r_lo2)
                test = 0
        else:
            # Xử lý nếu nghiệm không thể sửa được
            removed.fill(0)
            AdaptiveMechanism.update_score(operators, Config.PHI_3, destroy_score, destroy_used, repair_score, repair_used)

        # Vao dau moi segment, cap nhat trong so cac operator va tien hanh Local Search len nghiem hien tai
        if (i + 1) % ips == 0:
            AdaptiveMechanism.update_weight(destroy_operator, destroy_weight, destroy_score, destroy_used,
                                            repair_operator, repair_weight, repair_score, repair_used)
            LocalSearch.local_search_v2(solution, route_length, route_costs, distance_matrix)
            if sum(route_costs) < best_cost:
                best_sol, best_cost = np.copy(solution), sum(route_costs)

    # Khi tìm xong, in ra và trả về nghiệm tốt nhất tìm được
    print()
    print("Best cost:", best_cost)
    print(best_sol)
    return best_sol, best_cost




