import numpy as np
from Map import *
class QLearning:
    def __init__(self, grid, start, end, alpha=0.1, gamma=0.95, episodes=10000, lr=0.8):
        self.grid = grid
        self.start = start
        self.end = end
        self.alpha = alpha
        self.gamma = gamma
        self.episodes = episodes
        self.lr = lr
        self.q_table = {}

    def initialize_Q_U_table(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(dx))  # Số hành động = len(dx)

    def getV(self, q_values):
        # Hàm V dựa trên log-sum-exp
        v = self.alpha * np.log(np.sum(np.exp(q_values / self.alpha)))
        return v

    def choose_action(self, state):
        # Chọn hành động dựa trên phân phối softmax
        self.initialize_Q_U_table(state)
        q = self.q_table[state]
        v = self.getV(q)
        dist = np.exp((q - v) / self.alpha)
        action_probs = dist / np.sum(dist)
        action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
        return action

    def next_q(self, new_state):
        # Lấy giá trị Q của trạng thái kế tiếp
        self.initialize_Q_U_table(new_state)
        return self.q_table[new_state]

    def update(self, state, action, reward, next_state):
        # Cập nhật giá trị Q
        self.initialize_Q_U_table(state)
        self.initialize_Q_U_table(next_state)

        next_q_values = self.next_q(next_state)
        #print(next_state,next_q_values)
        target = reward + self.gamma * self.getV(next_q_values)
        self.q_table[state][action] += self.lr * (target - self.q_table[state][action])
    def improve(self, path):
        self.grid[self.end[0]][self.end[1]] = 1
        for i in range(len(path)-1):
            x, y = path[i]
            next_x, next_y = path[i+1]
            for j in range(4):
                if dx[j] == next_x-x and dy[j] == next_y-y:
                    reward = self.grid[next_x][next_y]
                    self.update((x,y), j, reward, (next_x,next_y))
        self.alpha = max(0.01, self.alpha * 0.99)

    def train(self):
        min_sum = N*N
        self.grid[self.end[0]][self.end[1]] = 1  # Đặt phần thưởng tại đích
        min_tau = 0.01  # Giá trị tối thiểu của τ
        tau_decay_rate = 0.99  # Tỷ lệ giảm của τ sau mỗi tập
        for episode in range(self.episodes):
            state = self.start
            sum = 1
            while state != self.end:
                #print(state)
                sum += 1
                action_idx = self.choose_action(state)  # Dùng softmax để chọn hành động
                next_state = (state[0] + dx[action_idx], state[1] + dy[action_idx])
                if 0 < next_state[0] <= N and 0 < next_state[1] <= N and self.grid[next_state[0]][next_state[1]] != -1:
                    reward = self.grid[next_state[0]][next_state[1]]
                    self.update(state, action_idx, reward, next_state)
                    state = next_state
                else:
                    reward = -0.3
                    self.update(state, action_idx, reward, next_state)

            # Giảm giá trị τ sau mỗi tập
            self.alpha = max(0.01, self.alpha * 0.99)
            min_sum = min(min_sum, sum)

            print(episode,sum)
        print(f"Đường đi ngắn nhất: {min_sum}")

    def print_path(self):

        current_state = self.start
        path = [current_state]

        while current_state != self.end:
            action_idx = np.argmax(self.q_table[current_state])

            next_state = (current_state[0] + dx[action_idx], current_state[1] + dy[action_idx])
            path.append(next_state)
            current_state = next_state
        return path
