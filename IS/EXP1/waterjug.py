# Water Jug Problem (3L, 7L) — measure 6L in either jug

CAP1, CAP2 = 3, 7
GOAL = 6

def goal_test(state):
    # state = (amount_in_3L, amount_in_7L)
    return GOAL in state

def move_gen(state):
    a, b = state
    moves = []

    # Fill actions
    if a < CAP1: moves.append((CAP1, b))
    if b < CAP2: moves.append((a, CAP2))

    # Empty actions
    if a > 0: moves.append((0, b))
    if b > 0: moves.append((a, 0))

    # Pour 3L -> 7L
    if a > 0 and b < CAP2:
        pour = min(a, CAP2 - b)
        moves.append((a - pour, b + pour))

    # Pour 7L -> 3L
    if b > 0 and a < CAP1:
        pour = min(b, CAP1 - a)
        moves.append((a + pour, b - pour))

    # Deduplicate while preserving order
    seen, clean = set(), []
    for m in moves:
        if m not in seen:
            seen.add(m)
            clean.append(m)
    return clean

# --- quick demo ---
if __name__ == "__main__":
    initial = (0, 0)
    print("Goal Test (0,6):", goal_test((0, 6)))
    print("Moves from (0,0):", move_gen(initial))

    # Optional: tiny BFS solver to verify we can reach 6L
    from collections import deque
    def bfs(start=(0,0)):
        q = deque([start])
        parent = {start: None}
        while q:
            s = q.popleft()
            if goal_test(s):
                path = []
                while s is not None:
                    path.append(s)
                    s = parent[s]
                return list(reversed(path))
            for ns in move_gen(s):
                if ns not in parent:
                    parent[ns] = s
                    q.append(ns)
        return None

    path = bfs(initial)
    print("One solution path:", path)