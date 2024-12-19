import random
from copy import deepcopy
from Map import *
import numpy as np

sv = []
# Định nghĩa Node
class Node:
    def __init__(self, state, action=None, pre_node=None):
        self.state = state  # Lưu trạng thái tại nút này
        self.action = action  # Lưu hành động dẫn đến trạng thái này
        self.pre_node = pre_node  # Nút cha
        self.children = dict()  # Các nút con
        self.is_expanded = False  # Trạng thái đã mở rộng chưa
        self.n = 1
        self.v = 0
        self.q = 0

    def add_child(self, action, state):
        # Thêm nút con mới với trạng thái mới và hành động mới
        if action not in self.children:
            child_node = Node(state, action, pre_node=self)
            self.children[action] = child_node
            return child_node
        return self.children[action]

# Định nghĩa MCTS
class MCTS:
    def __init__(self, grid, q_table, start, end, training=True):
        self.grid = grid  # Môi trường tìm đường
        self.start = start
        self.end = end
        self.copied_game = deepcopy(self.grid)  # Bản sao của môi trường để tránh thay đổi trạng thái gốc
        self.q_table = q_table  # Bảng Q-learning dùng để khởi tạo giá trị
        self.root = Node(start, None, None)  # Nút gốc với trạng thái bắt đầu
        self.training = training  # Chế độ huấn luyện

    def initialize_Q_U_table(self, state):
        if state not in self.q_table:
            # Nếu trạng thái chưa tồn tại, khởi tạo với giá trị mặc định (vd: mảng 0)
            self.q_table[state] = np.zeros(len(dx))

    def possible_actions(self, state):
        # Trả về các hành động hợp lệ từ trạng thái hiện tại
        actions = []
        x, y = state  # Lấy tọa độ của trạng thái hiện tại
        for i in range(4):  # 4 hướng di chuyển
            new_x = x + dx[i]
            new_y = y + dy[i]
            # Kiểm tra xem bước di chuyển có hợp lệ trong lưới không (từ (1, 1) tới (N, N))
            if 1 <= new_x <= N and 1 <= new_y <= N and self.grid[new_x][new_y] != -1:
                actions.append(i)  # Thêm chỉ số của hành động hợp lệ (0, 1, 2, hoặc 3)
        return actions

    def take_action(self, current_state, action):
        # Cập nhật trạng thái sau khi thực hiện hành động
        x, y = current_state

        # Tính toán tọa độ mới sau khi di chuyển
        new_x = x + dx[action]
        new_y = y + dy[action]

        # Cập nhật trạng thái trong lưới (nếu cần thiết)
        # Ví dụ: nếu có thể di chuyển đến (new_x, new_y), thì cập nhật current_state
        if 1 <= new_x <= N and 1 <= new_y <= N and self.grid[new_x][new_y] != -1:
            return (new_x, new_y)
        return current_state  # Nếu không thể di chuyển, giữ nguyên trạng thái hiện tại
    def selection(self, node):
        # Chọn đường đi từ nút gốc dựa trên UCT (Upper Confidence Bound for Trees)
        path = [node]
        while node.is_expanded and node.state!= self.end:
            action = max(node.children, key=lambda a: self.uct(node.children[a]))
            node = node.children[action]
            path.append(node)
        return path

    def expansion(self, path):
        current_state = self.get_state(path[-1])
        if current_state == self.end:
            return path
        cnt = self.possible_actions(current_state)
        if not path[-1].is_expanded:
            for action in cnt:  # Gọi trực tiếp trên self.grid
                # Tạo trạng thái con mới và thêm nút con
                new_state = (current_state[0] + dx[action], current_state[1] + dy[action])
                child_node = path[-1].add_child(action, new_state)
                # Tính giá trị cho q_table, nếu chưa có thì gán giá trị mặc định
                self.initialize_Q_U_table(current_state)
                child_node.q = self.q_table[current_state][action]
            path[-1].is_expanded = True
        action = random.choice(list(path[-1].children.keys()))
        path.append(path[-1].children[action])

        # Cập nhật trạng thái game đã thay đổi khi thực hiện hành động
        self.take_action(current_state, action)
        return path

    def simulation(self, path):
        # Đặt trạng thái ban đầu từ đường đi
        self.state = self.get_state(path[-1])
        while self.state != self.end:  # So sánh trạng thái với đích
            # Khởi tạo bảng Q nếu trạng thái chưa tồn tại
            self.initialize_Q_U_table(self.state)
            # Lấy hành động có giá trị Q lớn nhất
            q_values = self.q_table[self.state]
            action = np.argmax(q_values)  # Chọn hành động có giá trị Q lớn nhất

            # Cập nhật trạng thái sau khi thực hiện hành động
            self.state = self.take_action(self.state, action)  # Cập nhật trạng thái mới

            # Thêm trạng thái con vào cây tìm kiếm
            path[-1].add_child(action, self.state)

            # Thêm trạng thái con vào đường đi
            path.append(path[-1].children[action])

        return path

    def backpropagation(self, path):
        # Lan truyền ngược kết quả từ trạng thái cuối cùng về gốc
        for node in reversed(path):
            pre = node.pre_node
            if pre != None:
                pre.v = (pre.v*pre.n+node.q)/(pre.n+1)
            node.q = (node.q*node.n+0.95*node.v)/(node.n+1)
            node.n += 1

    def get_state(self, node):
        # Lấy trạng thái hiện tại từ nút, dựng lại từ đường đi trong cây
        return node.state

    def step(self, max_iterations=1000):
        # Thực hiện một bước trong quá trình tìm kiếm (selection -> expansion -> simulation -> backpropagation)
        for i in range(max_iterations):
            path = self.selection(self.root)
            expanded_path = self.expansion(path)
            simulated_path = self.simulation(expanded_path)
            self.backpropagation(simulated_path)
            self.copied_game = deepcopy(self.grid)  # Reset trạng thái bản sao
            if i == 999:
                for k in simulated_path:
                    state = k.state
                    x = int(state[0])
                    y = int(state[1])
                    fill_cell(x - 1, y - 1, green)
                    pygame.time.wait(100)
                for k in simulated_path:
                    state = k.state
                    x = int(state[0])
                    y = int(state[1])
                    fill_cell(x - 1, y - 1, white)  # Trả ô về màu trắng
                    draw_grid()
                pygame.time.wait(1000)
            print(i,len(simulated_path))
        # Sau khi tìm kiếm xong, chọn nút tốt nhất
    def uct(self, node, c=np.sqrt(2)):
        # Công thức UCT để cân bằng giữa khám phá và khai thác
        exploration = c * (np.sqrt(np.sqrt(node.pre_node.n) / node.n))
        return node.q + exploration
