import itertools

def goal_test(path, cities):
    # Goal: visited all cities exactly once
    return set(path) == set(cities) and len(path) == len(cities)

def move_gen(path, cities):
    # Generate next possible cities to visit
    return [path + [city] for city in cities if city not in path]

# Example usage:
cities = ["A", "B", "C", "D"]
path = ["A"]
print("Goal Test:", goal_test(["A", "B", "C", "D"], cities))
print("Moves from ['A']:", move_gen(path, cities))