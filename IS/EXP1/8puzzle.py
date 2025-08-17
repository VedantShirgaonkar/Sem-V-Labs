# 8 Puzzle — minimal BFS with step-by-step pretty printing
from collections import deque

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 = blank

def goal_test(state):
    return state == GOAL

def move_gen(state):
    """Return neighbors by sliding the blank Up, Down, Left, Right (if valid)."""
    s = list(state)
    idx = s.index(0)
    r, c = divmod(idx, 3)
    neighbors = []

    def swap_to(nr, nc):
        if 0 <= nr < 3 and 0 <= nc < 3:
            ni = nr * 3 + nc
            ns = s[:]
            ns[idx], ns[ni] = ns[ni], ns[idx]
            return tuple(ns)
        return None

    # Order: Up, Down, Left, Right
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ns = swap_to(r + dr, c + dc)
        if ns is not None:
            neighbors.append(ns)
    return neighbors

def pretty_print(state):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" ".join(str(x) if x != 0 else " " for x in row))
    print()

def action_between(a, b):
    """Describe which way the blank moved from a -> b."""
    ia, ib = a.index(0), b.index(0)
    ra, ca = divmod(ia, 3)
    rb, cb = divmod(ib, 3)
    if rb == ra - 1 and cb == ca: return "Up"
    if rb == ra + 1 and cb == ca: return "Down"
    if rb == ra and cb == ca - 1: return "Left"
    if rb == ra and cb == ca + 1: return "Right"
    return "?"

def bfs(start):
    start = tuple(start)
    q = deque([start])
    parent = {start: None}
    while q:
        s = q.popleft()
        if goal_test(s):
            # Reconstruct path
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

if __name__ == "__main__":
    # Your example initial state:
    initial = [1, 2, 3, 4, 5, 6, 0, 7, 8]

    print("Goal Test:", goal_test(tuple(initial)))
    print("\nSolving and printing path step-by-step:\n")
    path = bfs(initial)

    if not path:
        print("No solution found.")
    else:
        for i, st in enumerate(path):
            print(f"Step {i}:")
            pretty_print(st)
            if i < len(path) - 1:
                print("Move:", action_between(st, path[i+1]), "\n")