import random
N = 40
def generate_random_coordinates(maxX, maxY):
    # Sinh số lượng tọa độ ngẫu nhiên từ 1 đến 10
    num_coordinates = random.randint(244, 513)  # Số lượng tọa độ ngẫu nhiên
    coordinates = []

    for _ in range(num_coordinates):
        # Sinh tọa độ ngẫu nhiên trong khoảng (0, maxX) và (0, maxY)
        x = random.randint(1, maxX)
        y = random.randint(1, maxY)
        coordinates.append((x, y))  # Thêm tọa độ vào danh sách

    with open('obstacles/obstacles4.txt', 'w') as file:
        for x, y in coordinates:
            file.write(f"{x} {y}\n")  # Ghi từng tọa độ vào tệp

# Ví dụ sử dụng hàm
generate_random_coordinates(N,N)
