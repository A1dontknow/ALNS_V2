from numba import njit


@njit(cache=True)
def improve_v2(solution, route_length, route_costs, distance_matrix):
    for i in range(len(solution)):
        if route_length[i] >= 4:
            # Toi uu 1 tuyen xe bang cach xem xet viec dao cac duong cho nhau
            for x in range(1, route_length[i] - 3):
                for v in range(x + 1, route_length[i] - 2):
                    # Danh gia chi phi truoc va sau khi dao 2 duong
                    delta = distance_matrix[solution[i][x-1]][solution[i][v]] + distance_matrix[solution[i][x]][solution[i][v + 1]] - distance_matrix[solution[i][x-1]][solution[i][x]] - distance_matrix[solution[i][v]][solution[i][v + 1]]
                    if delta < -0.01:
                        # Trong truong hop chi phi co giam se doi 2 duong (not 2 khach hang)
                        a = x
                        b = v
                        route_costs[i] += delta
                        while a < b:
                            solution[i][a], solution[i][b] = solution[i][b], solution[i][a]
                            a += 1
                            b -= 1
                        return True
    return False


@njit(cache=True)
def local_search_v2(solution, route_length, route_costs, distance_matrix):
    """
    :param solution:
    :return: solution duoc cai tien boi local search

    Thuat toan local search (Hill climbing) su dung move 2-opt first improve
    """
    improved = True
    while improved:
        improved = improve_v2(solution, route_length, route_costs, distance_matrix)