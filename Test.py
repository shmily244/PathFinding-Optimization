import pygame

from GA import GeneticAlgorithm
from TabuSearch import TabuSearch
from QLearning import QLearning
from ACO import ACO
from MCTS import *
from PSO import *
from Map import *
pygame.init()
pygame.display.set_caption('Map')

screen.fill(white)  # Đặt nền màu trắng
draw_grid()
grid = [[0 for _ in range(N+1)] for _ in range(N+1)]

icon_energy = pygame.image.load('energy.jpg')
icon_energy = pygame.transform.scale(icon_energy, (cell_size - 10, cell_size - 10))
with open('energy3.txt', 'r') as file:
    for line in file:
        x, y = map(int, line.split())
        grid[x][y] = 0.01
        screen.blit(icon_energy, ((x-1) * cell_size+5, (y-1) * cell_size+5))
with open('obstacles/obstacles3.txt', 'r') as file:
    for line in file:
        x, y = map(int, line.split())
        grid[x][y] = -1
        fill_cell(x-1, y-1, black)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Nếu người dùng nhấn nút tắt
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                GA = GeneticAlgorithm(grid,(1,1),(N,N))
                GA.evolve()
            elif event.key == pygame.K_t:
                ts = TabuSearch(grid, (1,1), (N,N))
                initial_path = ts.random_path((1,1), [(N,N)],[])
                best_path = ts.improve_path(initial_path)
            elif event.key == pygame.K_p:
                psos = PSO(grid,(1,1),(N,N), 200)
                psoe = PSO(grid,(N,N),(1,1), 200)
                optimize(psos,psoe,100)
            elif event.key == pygame.K_a:
                aco = ACO(grid, (1, 1), (N, N))
                initial_path = []
                for i in range(50):
                    ts = TabuSearch(grid, (1, 1), (N, N))
                    initial_path.append(ts.random_path((1, 1), [(N, N)], []))
                    aco.update(initial_path)
                best_path = aco.run()
            elif event.key == pygame.K_q:
                ql = QLearning(grid, (1, 1), (N, N))
                for i in range(50):
                    ts = TabuSearch(grid, (1, 1), (N, N))
                    initial_path = ts.random_path((1, 1), [(N, N)], [])
                    best_path = ts.improve_path(initial_path)
                    ql.improve(best_path)
                    #print(i,len(best_path))
                ql.train()
                mcts = MCTS(grid,ql.q_table,(1,1),(N,N))
                mcts.step()

# Thoát Pygame
pygame.quit()