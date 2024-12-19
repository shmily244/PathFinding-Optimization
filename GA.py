import random

from Map import *
icon_energy = pygame.image.load('energy.jpg')
icon_energy = pygame.transform.scale(icon_energy, (cell_size - 10, cell_size - 10))
class Fitness:
    def __init__(self, grid, w_l=100, w_s1=1, w_s2=1):
        self.grid = grid
        self.w_l = w_l  # Trọng số độ dài đường đi
        self.w_s1 = w_s1  # Trọng số mức an toàn bậc 1
        self.w_s2 = w_s2  # Trọng số mức an toàn bậc 2

    def safety_penalty(self, path, level):
        """Tính mức phạt an toàn."""
        penalty = 0
        for x, y in path:
            if self.is_obstacle_nearby(x, y, level):
                penalty += 1
        return penalty

    def is_obstacle_nearby(self, x, y, level):
        """Kiểm tra xem có vật cản trong phạm vi level."""
        for i in range(-level, level + 1):
            for j in range(-level, level + 1):
                if 0 < x + i <= N and 0 < y + j <= N and self.grid[x + i][y + j] == -1:
                    return True
        return False

    def fitness(self,grid, path):
        """Tính giá trị fitness của đường đi."""
        l_p = len(path)  # Độ dài đường đi
        s1_p = self.safety_penalty(path, level=1)  # Mức an toàn bậc 1
        s2_p = self.safety_penalty(path, level=2)  # Mức an toàn bậc 2
        e = self.energy_penalty(grid,path)  # Mức phạt năng lượng
        # Tính giá trị fitness theo công thức
        return 1 / (self.w_l * l_p + self.w_s1 * s1_p + self.w_s2 * s2_p)-e

    def energy_penalty(self, grid, path):
        """Tính mức phạt năng lượng nếu robot rẽ."""
        penalty = 0
        for i in range(1, len(path) - 1):
            if grid[path[i][0]][path[i][1]]==1:
                penalty -= 1
            prev_direction = path[i][0] - path[i - 1][0] + path[i][1] - path[i - 1][1]
            next_direction = path[i + 1][0] - path[i][0] + path[i + 1][1] - path[i][1]
            if prev_direction != next_direction:
                penalty += 1
                if grid[path[i+1][0]][path[i+1][1]]==1:
                    penalty -= 1
        return penalty

class GeneticAlgorithm:
    def __init__(self, grid, start, end, pop_size=200):
        self.grid = grid
        self.start = start
        self.end = end
        self.pop_size = pop_size
        self.fitness_calculator = Fitness(grid)  # Đối tượng tính fitness
        self.population = self.initialize_population()
    def initialize_population(self):
        population = []
        for i in range(self.pop_size):
            path = self.random_path()
            if path[0] == self.start and path[-1] == self.end:
                population.append((path,self.fitness_calculator.fitness(self.grid,path)))
            else:
                i -= 1
        return population

    def random_path(self):
        c = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
        c[self.start[0]][self.start[1]] = 1
        path = [self.start]
        while True:
            cnt = 0
            for i in range(4):
                x = dx[i] + path[-1][0]
                y = dy[i] + path[-1][1]
                if 0 < x <= N and 0 < y <= N and c[x][y] ==0 and self.grid[x][y] >= 0:
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
            if x == self.end[0] and y == self.end[1]:
                break
        return path

    def select(self, population):
        """Chọn cá thể dựa trên độ thích nghi, đảm bảo không trùng fitness."""
        # Sắp xếp quần thể theo fitness giảm dần
        sorted_population = sorted(population, key=lambda x: x[1], reverse=True)

        # Dùng set để theo dõi các giá trị fitness đã gặp
        selected = []
        seen_fitness = set()

        for individual in sorted_population:
            if individual[1] not in seen_fitness:
                selected.append(individual)
                seen_fitness.add(individual[1])

            if len(selected) >= self.pop_size:
                break
        self.pop_size = len(selected)
        return selected
    def crossover(self,parent1, parent2):
        """Lai ghép hai cá thể."""
        child = []
        for i in range(1,len(parent1)-1):
            for j in range(1,len(parent2)-1):
                if parent1[i] == parent2[j]:
                    child1 = parent1[:i] + parent2[j:]
                    child2 = parent2[:j] + parent1[i:]
                    child.append(child1)
                    child.append(child2)
        return child
    def evolve(self):
        """Chạy thuật toán di truyền qua nhiều thế hệ."""
        for generation in range(10):
            for i in range(1,N+1):
                for j in range(1,N+1):
                    if self.grid[i][j] >0:
                        pos = ((i - 1) * cell_size + 5, (j - 1) * cell_size + 5)
                        screen.blit(icon_energy, pos)
            # Chọn lọc cá thể tốt nhất
            parents = self.select(self.population)
            # Lai ghép để tạo thế hệ mới
            children = []
            for i in range(self.pop_size):
                p1 = random.randint(0, self.pop_size//2)
                p2 = random.randint(0, self.pop_size-1)
                if p1 == p2:
                    continue
                child = self.crossover(parents[p1][0], parents[p2][0])
                for c in child:
                    children.append((c, self.fitness_calculator.fitness(self.grid,c)))
            # Cập nhật quần thể
            self.population = parents + children

            # In ra thế hệ tốt nhất mỗi lần lặp
            best = max(self.population, key=lambda x: x[1])
            print(f"Generation {generation + 1}: Best Fitness = {best[1]} Best Length = {len(best[0])}")
            for x,y in best[0]:
                fill_cell(x - 1, y - 1, green)
                pygame.time.wait(100)
            for x,y in best[0]:
                fill_cell(x - 1, y - 1, white)  # Trả ô về màu trắng
                draw_grid()
            pygame.time.wait(1000)

        # Trả về đường đi tốt nhất sau các thế hệ
        return max(self.population, key=lambda x: x[1])

