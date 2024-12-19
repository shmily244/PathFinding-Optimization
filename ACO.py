import numpy as np
import random
from Map import *

class ACO:
    def __init__(self, grid, start, end, n_ants=50, n_iterations=100, alpha=2, beta=3, evaporation_rate=0.3, pheromone_deposit=7):
        self.grid = grid
        self.start = start
        self.end = end
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha  # Ảnh hưởng của pheromone
        self.beta = beta  # Ảnh hưởng của heuristic
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit
        self.pheromone = np.ones_like(grid, dtype=float)  # Ma trận pheromone


    def is_valid_move(self, position):
        """Kiểm tra ô hợp lệ (không ra ngoài lưới hoặc gặp chướng ngại vật)."""
        x, y = position
        return 0 < x <=N and 0 < y <=N and self.grid[x][y] != -1

    def heuristic(self, position):
        """Hàm heuristic: Khoảng cách Manhattan đến đích."""
        return abs(position[0] - self.end[0]) + abs(position[1] - self.end[1])

    def choose_next_move(self, current_pos):
        """Chọn bước đi tiếp theo dựa trên pheromone và heuristic."""
        x, y = current_pos
        probabilities = []

        for i in range(len(dx)):
            next_pos = (x + dx[i], y + dy[i])
            if self.is_valid_move(next_pos):
                pheromone = self.pheromone[next_pos]
                heuristic = 1 / (self.heuristic(next_pos) + 1e-6)  # Tránh chia cho 0
                probabilities.append((next_pos, (pheromone ** self.alpha) * (heuristic ** self.beta)))

        if not probabilities:
            return None  # Không có bước đi hợp lệ

        # Chuẩn hóa xác suất
        total = sum(p[1] for p in probabilities)
        probabilities = [(p[0], p[1] / total) for p in probabilities]

        # Chọn bước đi dựa trên phân phối xác suất
        positions, probs = zip(*probabilities)
        return random.choices(positions, weights=probs, k=1)[0]

    def update_pheromone(self, paths):
        """Cập nhật pheromone: bốc hơi và thêm pheromone từ các đường đi."""
        self.pheromone *= (1 - self.evaporation_rate)  # Bốc hơi pheromone

        for path in paths:
            if len(path) > 1 and path[-1] == self.end:  # Chỉ thêm pheromone nếu đạt đích
                pheromone_contribution = self.pheromone_deposit / len(path)
                for pos in path:
                    self.pheromone[pos] += pheromone_contribution

    def update(self,paths):
        self.update_pheromone(paths)

    def run(self):
        best_path = None
        shortest_length = float('inf')

        for iteration in range(self.n_iterations):
            all_paths = []
            iteration_shortest = float('inf')

            for ant in range(self.n_ants):
                current_pos = self.start
                path = [current_pos]
                visited = set()
                visited.add(current_pos)

                while current_pos != self.end:
                    print(current_pos)
                    next_pos = self.choose_next_move(current_pos)
                    if next_pos is None:  # Không có bước đi hợp lệ
                        break
                    path.append(next_pos)
                    visited.add(next_pos)
                    current_pos = next_pos

                # Cập nhật đường tốt nhất trong vòng lặp
                if current_pos == self.end and len(path) < iteration_shortest:
                    iteration_shortest = len(path)

                if current_pos == self.end and len(path) < shortest_length:
                    best_path = path
                    shortest_length = len(path)

                all_paths.append(path)

            # Cập nhật pheromone
            self.update_pheromone(all_paths)

            print(f"Iteration {iteration + 1}/{self.n_iterations}, Shortest Path Length: {shortest_length} ")

        return best_path

