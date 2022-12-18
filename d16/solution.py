import itertools

## Helper methods
# Floyd Warshall Algorithm
def floydWarshall(adj_matrix): 
    dist = list(map(lambda i: list(map(lambda j: j, i)), adj_matrix))
    n = len(adj_matrix)
    for k in range(n):
      for i in range(n):
        for j in range(n):
          dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

def find_all_combinations_with_elephant(l):
  out = []
  for i in range(len(l) + 1):
    for subset in itertools.combinations(l, i):
      new = list(set(l) - set(list(subset)))
      out.append([new, list(subset)])
  return out[0:int(len(out)/2)]

class GraphExplorer:
  def __init__(self, max_minutes = 30):
    self.all_cost_candidate = []
    self.max_minutes = max_minutes
  
  def max_cost(self):
    l = self.all_cost_candidate
    max = 0
    for cand in l:
      if cand > max:
        max = cand
    return max
  
  def explore_graph_recursively(self, current_path, current_cost, current_min, all_valves, dist, remaining_non_null_nodes):
    if len(remaining_non_null_nodes) == 0:
      self.all_cost_candidate.append(current_cost)
      return
    for non_null_node in remaining_non_null_nodes:
      begin = current_path[-1]
      end = non_null_node
      distance = dist[all_valves[begin]["pos"]][all_valves[end]["pos"]]
      new_current_min = current_min + distance + 1
      if new_current_min > self.max_minutes:
        self.all_cost_candidate.append(current_cost)
        continue
      new_cost = current_cost + (self.max_minutes - new_current_min + 1) * all_valves[end]["flow"]
      tmp = remaining_non_null_nodes.copy()
      tmp.remove(end)
      new_path = current_path.copy()
      new_path.append(end)
      self.explore_graph_recursively(new_path, new_cost, new_current_min, all_valves, dist, tmp)

## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""),f.readlines()))

data = []
all_valves = {}
all_valves_list = []
non_null_valves = []
for idx, line in enumerate(lines):
  tmp = line.split("; tunnels lead to valves ") if "valves" in line else line.split("; tunnel leads to valve ")
  name = tmp[0].split("flow rate=")[0][6:8]
  flow = int(tmp[0].split("flow rate=")[1])
  neighbours = tmp[1].split(", ")
  all_valves[name] = {
    "flow": flow,
    "neighbours": neighbours,
    "pos": idx
  }
  all_valves_list.append(name)
  if flow > 0:
    non_null_valves.append(name)

# Compute adjacency matrix of the graph
n = len(lines)
adj_matrix = [[float('inf') for _j in range(n)] for _i in range(n)]
for i in range(n):
  valve_i = all_valves_list[i]
  for j in range(n):
    valve_j = all_valves_list[j]
    if valve_j in all_valves[valve_i]["neighbours"]:
      adj_matrix[i][j] = 1
    if i == j:
      adj_matrix[i][j] = 0

# Compute dist_matrix with dist_matrix[i][j] = shortest path distance between i and j
dist_matrix = floydWarshall(adj_matrix)

# Resolution
print("SOLUTION PART 1:")
e = GraphExplorer(30)
e.explore_graph_recursively(["AA"], 0, 1, all_valves, dist_matrix, non_null_valves)
print(e.max_cost())

print("SOLUTION PART 2:")
all_non_null_nodes_comb = find_all_combinations_with_elephant(non_null_valves)
max = 0
for combi in all_non_null_nodes_comb:
  e1 = GraphExplorer(26)
  e1.explore_graph_recursively(["AA"], 0, 1, all_valves, dist_matrix, combi[0])
  e2 = GraphExplorer(26)
  e2.explore_graph_recursively(["AA"], 0, 1, all_valves, dist_matrix, combi[1])
  count = e1.max_cost() + e2.max_cost()
  if count > max:
    max = count
print(max)
