import math
import heapq

def haversine(a, b):
    # a, b: (lat, lon) in degrees -> distance in kilometers
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    R = 6371.0
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(h))

def interpolate(a, b, t):
    return (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)

def make_route(name_prefix, start, end, count, lon_offset=0.0, lat_perturb=0.0):
    nodes = []
    for i in range(count):
        t = i/(count-1)
        lat, lon = interpolate(start, end, t)
        # add slight offsets to create distinct alternate paths
        lon += lon_offset * math.sin(t*math.pi)
        lat += lat_perturb * math.cos(t*2*math.pi)
        nodes.append({
            "name": f"{name_prefix}_{i+1}",
            "coord": (lat, lon)
        })
    return nodes

# Known endpoints: Juhu Beach -> Gateway of India (approx)
Juhu = (19.0886, 72.8264)
Gateway = (18.9220, 72.8347)

# Create two different plausible routes between the two places with intermediate checkpoints
route_coastal = make_route("Coastal", Juhu, Gateway, 22, lon_offset=0.008, lat_perturb=0.0012)
route_inland  = make_route("Inland",  Juhu, Gateway, 20, lon_offset=-0.006, lat_perturb=-0.0015)

# Add a few off-route (not-in-route) locations (5-8)
off_route = [
    {"name": "Powai_Lake", "coord": (19.1196, 72.8979)},
    {"name": "Bandra_Worli_Sealink_View", "coord": (19.015, 72.814)},
    {"name": "Aarey_Colony", "coord": (19.1395, 72.8799)},
    {"name": "Navi_Mumbai", "coord": (19.0330, 73.0297)},
    {"name": "Vashi_Park", "coord": (19.0760, 72.9980)},
    {"name": "Sanjay_Gandhi_NP", "coord": (19.2140, 72.9100)},
    {"name": "CST_Station", "coord": (18.9402, 72.8365)},
]

# Merge nodes and build index map
nodes = route_coastal + route_inland + off_route
for i, n in enumerate(nodes):
    n["id"] = i

id_by_name = {n["name"]: n["id"] for n in nodes}
coords = [n["coord"] for n in nodes]

# Build graph: connect sequentially along each route and add a few cross-links
graph = {n["id"]: {} for n in nodes}

def connect(a_id, b_id):
    d = haversine(coords[a_id], coords[b_id])
    graph[a_id][b_id] = d
    graph[b_id][a_id] = d

# Connect sequential nodes in coastal and inland routes
for route in (route_coastal, route_inland):
    for i in range(len(route)-1):
        a = route[i]["id"]; b = route[i+1]["id"]
        connect(a, b)

# Add some cross connections (alternative paths)
# Connect Bandra-like midpoints between routes to allow the algorithm choose the better path
cross_pairs = [
    (route_coastal[8]["id"], route_inland[7]["id"]),
    (route_coastal[12]["id"], route_inland[11]["id"]),
    (route_coastal[16]["id"], route_inland[14]["id"]),
    (route_coastal[4]["id"], route_inland[3]["id"]),
]
for a,b in cross_pairs:
    connect(a,b)

# Connect off-route nodes to nearest route nodes (within a sensible radius) to simulate side detours
for off in off_route:
    off_id = off["id"]
    # find 2 nearest route nodes and connect
    dists = sorted(((haversine(off["coord"], coords[i]), i) for i in range(len(coords))), key=lambda x: x[0])
    for dist, nid in dists[:2]:
        connect(off_id, nid)

# Helper: A* search
def a_star(start_id, goal_id):
    open_heap = []
    heapq.heappush(open_heap, (0.0, start_id))
    came_from = {}
    gscore = {start_id: 0.0}
    fscore = {start_id: haversine(coords[start_id], coords[goal_id])}

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal_id:
            # reconstruct path
            path = []
            cur = current
            while cur in came_from:
                path.append(cur)
                cur = came_from[cur]
            path.append(start_id)
            path.reverse()
            return path, gscore[current]

        for neighbor, w in graph[current].items():
            tentative_g = gscore[current] + w
            if tentative_g < gscore.get(neighbor, float('inf')):
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g
                f = tentative_g + haversine(coords[neighbor], coords[goal_id])
                fscore[neighbor] = f
                heapq.heappush(open_heap, (f, neighbor))
    return None, float('inf')

# Identify start and goal ids: use first node of coastal route as Juhu and last node of coastal route near Gateway
start_id = route_coastal[0]["id"]  # Juhu
# pick node with coords closest to Gateway as goal (to simulate Gateway of India)
goal_id = min(range(len(coords)), key=lambda i: haversine(coords[i], Gateway))

# Run A*
path_ids, total_km = a_star(start_id, goal_id)

# Present results
def pretty_path(path_ids):
    return " -> ".join(f"{nodes[i]['name']}" for i in path_ids)

if __name__ == "__main__":
    print("Start:", nodes[start_id]["name"], nodes[start_id]["coord"])
    print("Goal chosen:", nodes[goal_id]["name"], nodes[goal_id]["coord"])
    if path_ids:
        print("Shortest path (A* using Haversine):")
        print(pretty_path(path_ids))
        print(f"Total distance: {total_km:.3f} km")
    else:
        print("No path found.")
