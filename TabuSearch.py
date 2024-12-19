import random
from collections import deque
from Map import *
from GA import Fitness

class TabuSearch:
    def __init__(self, grid, start, end, tabu_size=1000, max_iter=1):
        self.grid = grid
        self.start = start
        self.end = end
        self.tabu_list = deque(maxlen=tabu_size)  # Danh sách tabu
        self.max_iter = max_iter  # Số lần lặp tối đa
        self.fitness_calculator = Fitness(grid)  # Đối tượng tính fitness
        self.best_cost = float('inf')  # Khởi tạo chi phí tốt nhất
        self.best_path = None  # Đường đi tốt nhất

    def random_path(self, start, end, tabu):
        """Tạo đường đi ngẫu nhiên từ start đến end."""
        c = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
        c[start[0]][start[1]] = 1
        for x, y in tabu:
            c[x][y] = 1
        path = [start]
        while True:
            if not path:
                return None
            if path[-1] in end:
                index = end.index(path[-1])  # Vị trí đầu tiên của path[-1] trong end
                merged_path = path + end[index + 1:]  # Ghép nối path với phần còn lại của end
                return merged_path
            cnt = 0
            for k in range(4):
                x = dx[k] + path[-1][0]
                y = dy[k] + path[-1][1]
                if 0 < x <= N and 0 < y <= N and c[x][y] == 0 and self.grid[x][y] >= 0:
                    cnt = 1
            if cnt == 0:
                path.pop()
                continue
            k = random.randint(0, 3)
            x = dx[k] + path[-1][0]
            y = dy[k] + path[-1][1]
            if 0 < x <= N and 0 < y <= N and (c[x][y] == 1 or self.grid[x][y] == -1):
                continue
            elif 0 < x <= N and 0 < y <= N:
                c[x][y] = 1
                path.append((x, y))
        return None

    def get_neighbors(self, position):
        """Lấy các ô lân cận hợp lệ."""
        x, y = position
        neighbors = []
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 < nx <= N and 0 < ny <= N and self.grid[nx][ny] >= 0:
                neighbors.append((nx, ny))
        return neighbors

    def improve_path(self, path):
        """Cải thiện đường đi bằng cách thay thế điểm và random bước kế tiếp."""
        current_path = path
        current_cost = self.fitness_calculator.fitness(self.grid,current_path)  # Tính chi phí đường đi hiện tại
        self.best_path = current_path
        for step in range(self.max_iter):
            # Chọn ngẫu nhiên một điểm trên đường đi (không phải start hoặc end)
            random_index = random.randint(1, len(current_path) - 2)
            current_point = current_path[random_index]
            # Lấy lân cận hợp lệ của điểm đó
            neighbors = self.get_neighbors(current_point)
            if not neighbors:
                continue  # Không có lân cận hợp lệ, bỏ qua bước này

            # Chọn lân cận ngẫu nhiên và tạo đường đi mới từ điểm đó đến end
            next_point = random.choice(neighbors)
            # Tạo đoạn đường mới từ next_point đến end
            new_path_segment = self.random_path(next_point,current_path[random_index+1:] ,current_path[:random_index+1])
            if not new_path_segment:
                continue

            # Nối đường đi mới vào vị trí gặp lại trong đường đi cũ
            reconnect_index = current_path.index(current_point)
            new_path = current_path[:reconnect_index+1] + new_path_segment
            # Tính chi phí của đường đi mới
            new_cost = self.fitness_calculator.fitness(self.grid,new_path)
            # Cập nhật nếu đường đi mới tốt hơn và không nằm trong danh sách tabu
            if new_cost > current_cost and new_path not in self.tabu_list:
                self.best_path= new_path
                self.best_cost = new_cost
                current_cost = new_cost  # Cập nhật chi phí hiện tại

            # Cập nhật danh sách tabu
            self.tabu_list.append(new_path)
            current_path = new_path
        return self.best_path