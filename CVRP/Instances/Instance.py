from sys import platform
import numpy as np
import re
import CVRP.Config as Config

"""
    :param file_name: File bai toan de giai

    Ham nay de dung cac thuoc tinh cho bai toan
        - optimal (float): Gia tri toi uu biet truoc
        - vehicles (int): So xe
        - capacity (int): Tai trong toi da cho phep moi xe
        - demand (np 1D): Nhu cau cua tung khach hang
        - x (np 1D): Toa do x cua tung khach hang
        - y (np 1D): Toa do y cua tung khach hang
        - distance_matrix (2D float): Ma tran khoang cach giua cac khach hang va kho voi nhau
        * Chu y: Kho se duoc quy uoc co chi so la 0 cho demand, x, y, distance_matrix. Khach hang
        se co ID tinh tu 1
"""


def load_data(file_name):
    f = None
    if platform == "linux" or platform == "linux2":
        try:
            f = open(Config.PROJECT_PATH + "/Dataset/" + file_name)
        except FileNotFoundError:
            try:
                f = open(Config.PROJECT_PATH + "/Dataset/" + file_name + ".txt")
            except FileNotFoundError:
                print("Ten file khong dung")
                exit(-1)
    elif platform == "win32":
        try:
            f = open(Config.PROJECT_PATH + "\\Dataset\\" + file_name)
        except FileNotFoundError:
            try:
                f = open(Config.PROJECT_PATH + "\\Dataset\\" + file_name + ".txt")
            except FileNotFoundError:
                print("Ten file khong dung")
                exit(-1)

    lines = f.readlines()
    line_two = re.findall(r'\d+', lines[1])
    # Input binh thuong co the khong co thong tin ve optimal
    try:
        optimal = int(line_two[1])
    except Exception:
        optimal = -1

    # Lay ra thong tin so luong xe, so khach hang va trong tai moi xe
    vehicles = int(line_two[0])
    dimensions = int(re.findall(r'\d+', lines[3])[0])
    capacity = int(re.findall(r'\d+', lines[5])[0])

    # Khoi tao toa do cua cac khach hang va nhu cau cua tung khach hang
    x = np.zeros(dimensions)
    y = np.zeros(dimensions)
    demand = np.zeros(dimensions)

    # Tu dong 8 lay thong tin vi tri kho, khach hang va nhu cau cua khach. Quy uoc kho luon co vi tri la 0
    for i in range(dimensions):
        demand[i] = int(lines[8 + dimensions + i].split().pop())
        node = lines[7 + i].split()
        y[i] = int(node.pop())
        x[i] = int(node.pop())

    distance_matrix = create_distance_matrix(x, y)

    return optimal, vehicles, capacity, demand, x, y, distance_matrix


# Tao ma tran khoang cach giua khach hang va depot voi nhau
def create_distance_matrix(x, y):
    matrix = np.hypot(x - x[0], y - y[0])
    for i in range(1, len(x)):
        matrix = np.vstack([matrix, np.hypot(x - x[i], y - y[i])])
    return matrix
