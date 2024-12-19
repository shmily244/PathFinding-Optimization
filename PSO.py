import numpy as np
import random
from Map import *
class Particle:
    def __init__(self, start, end, grid):
        self.grid = grid
        self.start = start
        self.end = end
        self.velocity = []  # Tạo danh sách rỗng trước
        self.position = self.random_path([start])  # Bắt đầu từ điểm start
        self.best_position = self.position
        self.best_length = N*N

    def random_path(self, st):
        c = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
        for x, y in st:
            c[x][y] = 1
        path = st
        while True:
            cnt = 0
            for i in range(4):
                x = dx[i] + path[-1][0]
                y = dy[i] + path[-1][1]
                if 0 < x <= N and 0 < y <= N and c[x][y] ==0 and self.grid[x][y] == 0:
                    cnt = 1
            if cnt == 0:
                path.pop()
                self.velocity.pop()
                continue
            k = random.randint(0, 3)
            x = dx[k] + path[-1][0]
            y = dy[k] + path[-1][1]
            if 0 < x <= N and 0 < y <= N and (c[x][y] == 1 or self.grid[x][y] == -1):
                continue
            elif 0 < x <= N and 0 < y <= N:
                c[x][y] = 1
                path.append((x, y))
                self.velocity.append((dx[i],dy[i]))
            if x == self.end[0] and y == self.end[1]:
                break
        return path

    def update_velocity(self, global_best_position, inertia=0.5, cognitive=1.5, social=1.5):
        """Cập nhật vận tốc dựa trên vị trí tốt nhất của hạt và vị trí tốt nhất toàn cục."""
        if len(self.position) == 1:
            return self.velocity # Nếu chỉ có ô start thì không cần cập nhật vận tốc nữa
        new_velocity = []
        for i in range(len(self.position)-1):
            # Lấy các thành phần vận tốc dựa trên vị trí hiện tại, tốt nhất của hạt và tốt nhất toàn cục
            if i >=len(self.best_position):
                dx_cognitive = cognitive * random.random() * (-self.position[i][0])
                dy_cognitive = cognitive * random.random() * (-self.position[i][1])
            else:
                dx_cognitive = cognitive * random.random() * (self.best_position[i][0] - self.position[i][0])
                dy_cognitive = cognitive * random.random() * (self.best_position[i][1] - self.position[i][1])
            cognitive_component = (dx_cognitive, dy_cognitive)
            # Tính động cơ xã hội cho mỗi chiều x và y
            if i>=len(global_best_position):
                dx_social = social * random.random() * (-self.position[i][0])
                dy_social = social * random.random() * (-self.position[i][1])
            else:
                dx_social = social * random.random() * (global_best_position[i][0] - self.position[i][0])
                dy_social = social * random.random() * (global_best_position[i][1] - self.position[i][1])
            # Cập nhật thành phần vận tốc xã hội
            social_component = (dx_social, dy_social)

            # Cập nhật inertia_component cho từng chiều (x, y)
            inertia_component = (inertia * self.velocity[i][0], inertia * self.velocity[i][1]) if i < len(
                self.velocity) else (0, 0)

            # Cộng tất cả các thành phần lại (inertia, cognitive, social) cho từng chiều (x, y)
            new_velocity.append((
                inertia_component[0] + cognitive_component[0] + social_component[0],  # Cộng cho chiều x
                inertia_component[1] + cognitive_component[1] + social_component[1]  # Cộng cho chiều y
            ))

        self.velocity = new_velocity

    def update_position(self):
        """Cập nhật vị trí hạt dựa trên vận tốc."""
        c = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
        c[self.position[0][0]][self.position[0][1]] = 1
        new_position = [self.position[0]]
        for v in self.velocity:
            if abs(v[0]) > abs(v[1]):
                # Di chuyển theo hướng x
                next_x = new_position[-1][0] + (1 if v[0] > 0 else -1)
                next_y = new_position[-1][1]
            else:
                # Di chuyển theo hướng y
                next_x = new_position[-1][0]
                next_y = new_position[-1][1] + (1 if v[1] > 0 else -1)
            # Kiểm tra nếu vị trí mới nằm trong lưới và không phải chướng ngại vật
            if 0 < next_x <=N and 0 < next_y <= N and self.grid[next_x][next_y] !=-1 and c[next_x][next_y] != 1 :
                new_position.append((next_x, next_y))
                c[next_x][next_y] = 1

            # Dừng nếu đã đến điểm đích
            if new_position[-1] == self.end:
                break
        if new_position[-1] == self.end:
            self.position = new_position
        else:
            self.position = self.random_path(new_position)

    def evaluate(self):
        """Tính toán fitness cho hạt."""
        length = len(self.position)
        if length < self.best_length:
            self.best_length = length
            self.best_position = self.position[:]


class PSO:
    def __init__(self, grid, start, end, num_particles):
        self.grid = grid
        self.start = start
        self.end = end
        self.particles = [Particle(start,end,grid) for _ in range(num_particles)]
        self.global_best_position = None
        self.global_best_length = N*N
    def update(self):
        for particle in self.particles:
            # Đánh giá fitness của từng hạt
            particle.evaluate()
            # Cập nhật vị trí tốt nhất toàn cục
            if particle.best_length < self.global_best_length:
                self.global_best_position = particle.best_position
                self.global_best_length = particle.best_length
        for particle in self.particles:
            # Cập nhật vận tốc và vị trí hạt
            particle.update_velocity(self.global_best_position)
            particle.update_position()
def merge(a,b):
    length = min(len(a),len(b))
    if length == len(a):
        s = a
    else:
        s = b
    c = b[::-1]
    for i in range(len(a)):
        if a[i] in c:
            m = a[:i]+c[c.index(a[i]):]
            if len(m)<length:
                length = len(m)
                s = m
    return s

def optimize(a, b, max_iter=100):
    """Chạy quá trình tối ưu PSO."""
    best_length = N * N
    for generation in range(max_iter):
        a.update()
        b.update()
        best = merge(a.global_best_position, b.global_best_position)
        if best!= None and len(best)<best_length:
            best_length = len(best)
            print(f"Generation {generation + 1}: Best Length = {len(best)}")
            print(best)
            for x, y in best:
                fill_cell(x - 1, y - 1, green)
                pygame.time.wait(100)
            for x, y in best:
                fill_cell(x - 1, y - 1, white)  # Trả ô về màu trắng
                draw_grid()
            pygame.time.wait(1000)

