ROWS, COLS = 3, 3

def print_state(state):
    for i in range(ROWS):
        print(state[i*COLS:(i+1)*COLS])
    print()

def is_goal(state):
    return state == (1,2,3,4,5,6,7,8,0)

def movegen(state):
    s = list(state)
    i = s.index(0)
    r, c = divmod(i, COLS)
    moves = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            t = s[:]
            j = nr*COLS + nc
            t[i], t[j] = t[j], t[i]
            moves.append(tuple(t))
    return moves

def _dls(start, depth_bound):
    stack = [(start, -1, 0)]
    chain = []
    while stack:
        state, parent_idx, depth = stack.pop()
        chain = chain[:parent_idx+1]
        chain.append(state)
        if is_goal(state):
            return chain[:]
        if depth < depth_bound:
            children = [c for c in movegen(state) if c not in set(chain)]
            for child in reversed(children):
                stack.append((child, len(chain)-1, depth+1))
    return None

def iddfs(start, max_depth=50):
    for depth in range(max_depth+1):
        path = _dls(start, depth)
        if path is not None:
            return path
    return None

def is_solvable(state):
    a = [x for x in state if x != 0]
    inv = 0
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            if a[i] > a[j]:
                inv += 1
    return inv % 2 == 0

if __name__ == "__main__":
    start_state = (1,2,3,4,5,6,7,0,8)
    print("Start State:")
    print_state(start_state)
    if not is_solvable(start_state):
        print("Puzzle is not solvable.")
    else:
        path = iddfs(start_state, max_depth=10)
        if path:
            print(f"Solution found in {len(path)-1} moves!")
            for step, st in enumerate(path):
                print(f"Step {step}:")
                print_state(st)
        else:
            print("No solution found.")