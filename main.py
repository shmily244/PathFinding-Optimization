from Dijkstra import *
from Astar import *
from BFS import *
import pandas as pd
# Khởi tạo Pygame
pygame.init()

N = 20
start = (1,1)
end = (N,N)
# Tạo cửa sổ màn hình
pygame.display.set_caption('Map')

screen.fill(white)  # Đặt nền màu trắng
draw_grid()

icon_start = pygame.image.load('start.jpg')  # Thay thế bằng đường dẫn tới tệp hình ảnh của bạn
icon_end = pygame.image.load('end.jpg')
icon_energy = pygame.image.load('energy.jpg')
icon_monster = pygame.image.load('monster.jpg')
# Thay đổi kích thước biểu tượng (Giả sử bạn muốn thu nhỏ về kích thước ô)
icon_start = pygame.transform.scale(icon_start, (cell_size - 10, cell_size - 10))  # Giảm kích thước xuống
icon_end = pygame.transform.scale(icon_end, (cell_size - 10, cell_size - 10))
icon_energy = pygame.transform.scale(icon_energy, (cell_size - 10, cell_size - 10))
icon_monster = pygame.transform.scale(icon_monster, (cell_size - 10, cell_size - 10))

grid = [[0 for _ in range(N+1)] for _ in range(N+1)]

with open('obstacles/obstacles2.txt', 'r') as file:
    for line in file:
        x, y = map(int, line.split())
        grid[x][y]=-1
        fill_cell(x-1, y-1, black)
with open('monster.txt', 'r') as file:
    for line in file:
        x, y = map(int, line.split())
        pos = ((x - 1) * cell_size + 5, (y - 1) * cell_size + 5)
        screen.blit(icon_monster, pos)
grid[start[0]][start[1]] = 1
grid[end[0]][end[1]] = 1
energy = []
c = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
p = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
energy.append(start)
p[start[0]][start[1]] = 0
cnt = 1
with open('energy2.txt', 'r') as file:
    for line in file:
        x, y = map(int, line.split())
        grid[x][y] = 1
        pos = ((x-1) * cell_size + 5, (y-1) * cell_size + 5)
        screen.blit(icon_energy, pos)
        energy.append((x,y))
        p[x][y] = cnt
        cnt += 1
energy.append(end)
p[end[0]][end[1]] = len(energy)-1

posstart = ((start[0]-1) * cell_size + 5, (start[1]-1) * cell_size + 5)
screen.blit(icon_start, posstart)
posend = ((end[0]-1) * cell_size + 5, (end[1]-1) * cell_size + 5)
screen.blit(icon_end, posend)

graph = []
edge = BFS(grid,start)
for u,v,w in edge:
    graph.append((u,v,w))
    c[p[u[0]][u[1]]][p[v[0]][v[1]]] = w

for x in range(1,N+1):
    for y in range(1,N+1):
        if grid[x][y]>0:
            edge = BFS(grid,(x,y))
            for u, v, w in edge:
                graph.append((u, v, w))
                c[p[u[0]][u[1]]][p[v[0]][v[1]]] = w

x = [0 for i in range(N)]
pre = [0 for i in range(N)]
stt = [0 for i in range(N)]
ans = float('inf')
def cal(i,sum):
    global ans
    if i > 8:
        if sum+c[x[i-1]][9] < ans:
            ans = sum+c[x[i-1]][9]
            for k in range(9):
                stt[k] = x[k]
        return
    for j in range(1,9):
        if pre[j]:
            continue
        x[i] = j
        pre[j] = i
        cal(i+1,sum + c[x[i-1]][j])
        pre[j] = 0

a = {}
s = set()
for i in range(1,N+1):
    for j in range(1,N+1):
        a[(i,j)] = []
for u,v,w in graph:
    a[u].append((v, w))
    a[v].append((u, w))
    s.add(v)

# Vòng lặp chính

cal(1, 0)
ans += go(grid,run(grid,energy[stt[1]]),start,energy[stt[1]])
stt[9] = 9
for i in range(1,9):
    ans+= go(grid, run(grid, energy[stt[i+1]]),energy[stt[i]], energy[stt[i+1]])
print(ans)
found_path = "NO"
if ans>0:
    found_path = "YES"
df = pd.DataFrame({'ans': [ans], 'found_path': [found_path]})  # Tạo DataFrame với giá trị ans và found_path
df.to_csv('results.csv', mode='a', index=False, header=False)  # Ghi vào file CSV
