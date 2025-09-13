import heapq

start_state = (('D', 'C', 'B', 'A'), ('F', 'E'))
goal_state  = (('D', 'C', 'B', 'E', 'A'), ('F',))


def heuristic_1(state, goal):
    """Counts the total number of blocks that are in the wrong place."""
    misplaced = 0
    goal_block_positions = {block: stack for stack in goal for block in stack}
    
    for stack in state:
        for block in stack:
            if block not in goal_block_positions or stack != goal_block_positions[block]:
                misplaced += 1
    return misplaced

def heuristic_2(state, goal):
    """Counts the number of stacks that are not perfectly correct."""
    correct_stacks = 0
    for s_stack in state:
        if s_stack in goal:
            correct_stacks += 1
    return len(goal) - correct_stacks


def get_successors(state):
    """Generates all possible next states."""
    successors = []
    state_list = [list(s) for s in state]

    for i, source_stack in enumerate(state_list):
        if not source_stack:
            continue
        
        # Move to other stacks
        for j, dest_stack in enumerate(state_list):
            if i == j:
                continue
            
            temp_state = [list(s) for s in state_list]
            block = temp_state[i].pop()
            temp_state[j].append(block)
    
            new_state = tuple(tuple(s) for s in temp_state if s)
            successors.append(new_state)
            
        # Move to a new stack
        temp_state = [list(s) for s in state_list]
        block = temp_state[i].pop()
        new_state = tuple(tuple(s) for s in temp_state if s) + ((block,),)
        successors.append(new_state)
        
    return successors


def best_first_search(start, goal, heuristic):
    """Finds a path from start to goal using a heuristic."""
    # The open list is a priority queue of (heuristic_value, path)
    open_list = [(heuristic(start, goal), [start])]
    closed_set = set()

    while open_list:
        _, path = heapq.heappop(open_list)
        current = path[-1]

        if current == goal:
            return path  # Success!

        if current in closed_set:
            continue
        closed_set.add(current)

        for successor in get_successors(current):
            if successor not in closed_set:
                new_path = path + [successor]
                heapq.heappush(open_list, (heuristic(successor, goal), new_path))
    
    return None # Failure

def hill_climbing(start, goal, heuristic):
    """Tries to find the goal by always choosing the best next move."""
    current = start
    while True:
        successors = get_successors(current)
        if not successors:
            break
        
        best_successor = min(successors, key=lambda s: heuristic(s, goal))

        # If the best next step is not better than where we are, stop.
        if heuristic(best_successor, goal) >= heuristic(current, goal):
            break
        
        current = best_successor
    return current

print("--- Best-First Search ---")

print("\nUsing Heuristic 1 (count misplaced blocks):")
path1 = best_first_search(start_state, goal_state, heuristic_1)
if path1:
    print(f"Path found in {len(path1) - 1} moves.")
    for step in path1:
        print(f"  -> {step}")
else:
    print("No path found.")


print("\nUsing Heuristic 2 (count incorrect stacks):")
path2 = best_first_search(start_state, goal_state, heuristic_2)
if path2:
    print(f"Path found in {len(path2) - 1} moves.")
else:
    print("No path found.") # This heuristic is not good enough to find the path


print("\n\n--- Hill Climbing ---")

print("\nUsing Heuristic 1 (count misplaced blocks):")
final_state1 = hill_climbing(start_state, goal_state, heuristic_1)
print(f"Final state reached: {final_state1}")
print("Goal Reached!" if final_state1 == goal_state else "Did not reach goal.")

print("\nUsing Heuristic 2 (count incorrect stacks):")
final_state2 = hill_climbing(start_state, goal_state, heuristic_2)
print(f"Final state reached: {final_state2}")
print("Goal Reached!" if final_state2 == goal_state else "Did not reach goal.")