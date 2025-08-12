from collections import deque

# State = (jug8, jug5, jug3)
def goal_test(a, b, c):
    return a == 4 or b == 4 or c == 4

def move_gen(a, b, c):
    moves = []
    max8, max5, max3 = 8, 5, 3

    # Fill
    moves.append((max8, b, c))
    moves.append((a, max5, c))
    moves.append((a, b, max3))

    # Empty
    moves.append((0, b, c))
    moves.append((a, 0, c))
    moves.append((a, b, 0))

    # Pour between jugs
    # 8 → 5
    pour = min(a, max5 - b)
    moves.append((a - pour, b + pour, c))

    # 8 → 3
    pour = min(a, max3 - c)
    moves.append((a - pour, b, c + pour))

    # 5 → 8
    pour = min(b, max8 - a)
    moves.append((a + pour, b - pour, c))

    # 5 → 3
    pour = min(b, max3 - c)
    moves.append((a, b - pour, c + pour))

    # 3 → 8
    pour = min(c, max8 - a)
    moves.append((a + pour, b, c - pour))

    # 3 → 5
    pour = min(c, max5 - b)
    moves.append((a, b + pour, c - pour))

    return moves

# Start: 8L full, 5L empty, 3L empty
start = (8, 0, 0)
q = deque([start])
visited = {start}

while q:
    a, b, c = q.popleft()
    print((a, b, c))

    if goal_test(a, b, c):
        print("Goal reached!")
        break

    for next_state in move_gen(a, b, c):
        if next_state not in visited:
            visited.add(next_state)
            q.append(next_state)