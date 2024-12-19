import heapq
N = 20
trace = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
def Dijkstra(a, start, end):
    visited = [[float('inf') for _ in range(N+1)] for _ in range(N+1)]
    visited[start[0]][start[1]] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        k, node = heapq.heappop(priority_queue)
        if visited[node[0]][node[1]] != k:
            continue
        if node[0] == end[0] and node[1] == end[1]:
            print(k)
        for i,w in a[node]:
            if visited[i[0]][i[1]] >= visited[node[0]][node[1]]+w:
                visited[i[0]][i[1]] = visited[node[0]][node[1]]+w
                trace[i[0]][i[1]] = node
                heapq.heappush(priority_queue, (visited[i[0]][i[1]], (i[0], i[1]) ))







