from numba import njit
import numpy as np
import CVRP.Config as Config


@njit(cache=True)
def numba_choice(population, weights, k):
    """
    Hàm này chủ yếu lấy ngẫu nhiên phần tử trong mảng dựa trên trọng số. Stolen from stackoverflow
    """
    # Get cumulative weights
    wc = np.cumsum(weights)
    # Total of weights
    m = wc[-1]
    # Arrays of sample and sampled indices
    sample = np.empty(k, population.dtype)
    sample_idx = np.full(k, -1, np.int32)
    # Sampling loop
    i = 0
    while i < k:
        # Pick random weight value
        r = m * np.random.rand()
        # Get corresponding index
        idx = np.searchsorted(wc, r, side='right')
        # Check index was not selected before
        # If not using Numba you can just do `np.isin(idx, sample_idx)`
        for j in range(i):
            if sample_idx[j] == idx:
                continue
        # Save sampled value and index
        sample[i] = population[idx]
        sample_idx[i] = population[idx]
        i += 1
    return sample


@njit(cache=True)
def select_operator(destroy_operator, destroy_weight, repair_operator, repair_weight):
    """
    :return: Tra ve 1 cap destroy - repair operator theo co che roulette-wheel (uu tien chon operator co trong so cao)
    """
    return numba_choice(destroy_operator, destroy_weight, 1), numba_choice(repair_operator, repair_weight, 1)


@njit(cache=True)
def update_score(operator, phi, destroy_score, destroy_used, repair_score, repair_used):
    """
    Ham update diem dua tren performance phi va so lan da su dung operator
    """
    destroy_score[operator[0]] += phi
    destroy_used[operator[0]] += 1
    repair_score[operator[1]] += phi
    repair_used[operator[1]] += 1


@njit(cache=True)
def update_weight(destroy_operator, destroy_weight, destroy_score, destroy_used, repair_operator, repair_weight, repair_score, repair_used):
    """
    :return:

    Ham update trong so cua cac operator dua tren past performance
    Mô tả công thức:
    - N: Hệ số phản ứng
    - w: Trọng số hiện tại của operator
    - pi: Điểm mà operator đó tích lũy được
    - o: Số lần đã dùng
    """
    # Update destroy
    for i in range(len(destroy_operator)):
        if destroy_used[i] != 0:
            w = destroy_weight[i]
            pi = destroy_score[i]
            o = destroy_used[i]
            destroy_weight[i] = (1 - Config.N) * w + Config.N * pi / (Config.V * o)

    # Update repair
    for i in range(len(repair_operator)):
        if repair_used[i] != 0:
            w = repair_weight[i]
            pi = repair_score[i]
            o = repair_used[i]
            repair_weight[i] = (1 - Config.N) * w + Config.N * pi / (Config.V * o)

    # Reset het diem va so lan da dung
    destroy_score.fill(0)
    repair_score.fill(0)
    destroy_used.fill(0)
    repair_used.fill(0)
