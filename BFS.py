from collections import deque
from Map import *
import time
import random
N = 20
dx = [1,-1,0,0]
dy = [0,0,-1,1]

def BFS(grid, start, end = False, kt = False):
    tracee = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
    edge =[]
    visited = [[1 for _ in range(N + 1)] for _ in range(N + 1)]
    visited[start[0]][start[1]] = 0
    dq = deque()
    dq.append((0,start[0], start[1]))
    while dq:
        node = dq.popleft()
        if end and node[1] == end[0] and node[2] == end[1]:
            if kt:
                while True:
                    end = tracee[end[0]][end[1]]
                    if end == start:
                        break
                    fill_cell(end[0]-1,end[1]-1,green)
                    pygame.time.wait(1000)
            return edge
        for i in range(4):
            nx = node[1] + dx[i]
            ny = node[2] + dy[i]
            if 0 < nx <= N and 0 < ny <= N and visited[nx][ny] == 1 and grid[nx][ny] >= 0:
                if kt:
                    tracee[nx][ny] = (node[1],node[2])
                visited[nx][ny] = visited[node[1]][node[2]]-1
                dq.append((visited[nx][ny],nx,ny))
                if grid[nx][ny] >= 0:
                    n = (nx,ny)
                    edge.append((start,n,-visited[nx][ny]))
    return edge

def run(grid,start):
    visited = [[-1 for _ in range(N + 1)] for _ in range(N + 1)]
    visited[start[0]][start[1]] = 0
    dq = deque()
    dq.append((0, start[0], start[1]))
    while dq:
        node = dq.popleft()

        for i in range(4):
            nx = node[1] + dx[i]
            ny = node[2] + dy[i]
            if 0 < nx <= N and 0 < ny <= N and visited[nx][ny] == -1 and grid[nx][ny] >= 0:
                visited[nx][ny] = visited[node[1]][node[2]] + 1
                dq.append((visited[nx][ny], nx, ny))
    return visited

icon_start = pygame.image.load('start.jpg')
icon_start = pygame.transform.scale(icon_start, (cell_size - 10, cell_size - 10))
icon_monster = pygame.image.load('monster.jpg')
icon_monster = pygame.transform.scale(icon_monster, (cell_size - 10, cell_size - 10))
monster =[]
with open('monster.txt', 'r') as file:
    for line in file:
        x, y = map(int, line.split())
        monster.append((x,y))
def go(grid, visited, start, end):
    sum = 0
    while start != end:
        sum += 1
        ansv = float('inf')
        ansx = 0
        ansy = 0
        for i in range(4):
            nx = start[0] + dx[i]
            ny = start[1] + dy[i]
            kt = True
            for x, y in monster:
                if abs(nx - x) + abs(ny - y) <= 1:
                    kt = False
            if 0 < nx <= N and 0 < ny <= N and kt and grid[nx][ny]>=0 and 0 <= visited[nx][ny]<= ansv:
                ansv = visited[nx][ny]
                ansx = nx
                ansy = ny
        fill_cell(start[0] - 1, start[1] - 1, white)  # Trả ô về màu trắng
        draw_grid()
        if ansx == 0 and ansy == 0:
            return -float('inf')
        start = (ansx,ansy)
        pos = ((start[0] - 1) * cell_size + 5, (start[1] - 1) * cell_size + 5)
        screen.blit(icon_start, pos)
        pygame.display.flip()
        for i in range(len(monster)):
            num = random.randint(0, 3)
            nx = monster[i][0] + dx[num]
            ny = monster[i][1] + dy[num]
            if 0 < nx <= N and 0 < ny <= N and grid[nx][ny] == 0:
                fill_cell(monster[i][0] - 1, monster[i][1] - 1, white)  # Trả ô về màu trắng
                draw_grid()
                monster[i] = (nx,ny)
                pos = ((nx-1) * cell_size + 5, (ny-1) * cell_size + 5)
                screen.blit(icon_monster, pos)
                pygame.display.flip()

        pygame.time.wait(1000)
    return sum