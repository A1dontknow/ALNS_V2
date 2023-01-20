from CVRP.Algorithm.ALNS import solve_v2
from CVRP.Instances.Instance import load_data
import matplotlib.pyplot as plt
import time
import CVRP.Config as Config
import os


def main():
    print("ALNS for Vehicle Routing Problem")
    print("--------------------------------")
    print("Ban hay nhap ten file trong thu muc CVRP\\Dataset de giai.\nLuu y: File ban can giai can "
          "co dinh dang khop voi cac file trong thu muc <ProjectPath>\\CVRP\\Dataset\\. Vi du: \"A-n36-k5\"")
    file = input()
    # Khoi tao instance cho bai toan
    optimal, vehicles, capacity, demand, x, y, distance_matrix = load_data(file)
    print("----------------------------------------------------")

    # Dung ALNS de solve
    best, cost = solve_v2(vehicles, capacity, demand, distance_matrix)

    # Luu nghiem tot nhat vao file
    t = time.localtime()
    current_time = time.strftime("%H_%M_%S", t)
    if not os.path.exists(Config.PROJECT_PATH + "\\Dataset\\Solution\\" + file.split(".txt")[0]):
        os.mkdir(Config.PROJECT_PATH + "\\Dataset\\Solution\\" + file.split(".txt")[0])
    f = open(Config.PROJECT_PATH + "\\Dataset\\Solution\\" + file.split(".txt")[0] + "\\" + current_time + ".txt",
             "wt")
    f.write(str(cost))
    f.write(str(best))
    f.close()

    # Minh hoa bang matplotlib va save anh
    for route in best:
        a = []
        b = []
        z = 0
        for node in route:
            if node == 0:
                z += 1
            a.append(x[node])
            b.append(y[node])
            if z == 2:
                break

        plt.plot(a, b)
        plt.plot(a, b, 'or')
        plt.plot(x[0], y[0], "sk")
    plt.title("VRP Solution (Cost = " + str("%.2f" % cost) + ")")
    plt.savefig(
        Config.PROJECT_PATH + "\\Dataset\\Solution\\" + file.split(".txt")[0] + "\\" + current_time + ".png")
    print("Anh va file da duoc luu vao trong thu muc <ProjectPath>\\CVRP\\Dataset\\Solution\\<Ten file>\\")
    plt.show()


if __name__ == '__main__':
    main()
