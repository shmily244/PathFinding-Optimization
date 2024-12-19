import heapq

N = 20
traca = [[0 for _ in range(N + 1)] for _ in range(N + 1)]


def heuristic(a, b):
    # Sử dụng khoảng cách Manhattan làm hàm ước lượng
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def Astar(a, start, end):
    visited = [[float('inf') for _ in range(N + 1)] for _ in range(N + 1)]
    visited[start[0]][start[1]] = 0
    priority_queue = [(0 + heuristic(start, end), start)]  # Tổng chi phí + heuristic

    while priority_queue:
        total_cost, node = heapq.heappop(priority_queue)
        current_cost = visited[node[0]][node[1]]

        if current_cost != total_cost - heuristic(node, end):
            continue

        if node[0] == end[0] and node[1] == end[1]:
            print(current_cost)
            return

        for (i, w) in a[node]:
            new_cost = current_cost + w
            if visited[i[0]][i[1]] >= new_cost:  # Nếu có chi phí cao hơn
                visited[i[0]][i[1]] = new_cost
                traca[i[0]][i[1]] = node
                # Thêm vào hàng đợi với tổng chi phí (cost + heuristic)
                heapq.heappush(priority_queue, (new_cost + heuristic(i, end), (i[0], i[1])))

