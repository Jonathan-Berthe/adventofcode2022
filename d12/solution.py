import string

with open('./input.txt') as f:
  lines = list(map(lambda line: list(line.replace("\n", "")),f.readlines()))

class Graph:
  def __init__(self, height_matrix, sdeb, sfin, part1 = True):
    self.height_matrix = height_matrix
    self.m = len(height_matrix)
    self.n = len(height_matrix[0])
    self.sdeb = sdeb
    self.sfin = sfin
    self.weight_matrix = [[float('inf') for _j in range(self.n)] for _i in range(self.m)]
    self.weight_matrix[sdeb[0]][sdeb[1]] = 0
    self.part1 = part1
    self.previous_nodes = [[None for _j in range(self.n)] for _i in range(self.m)]
    self.queue = { sdeb }

  def run_dijkstra(self):
    while True:
      min_node = self.find_min_in_queue()
      self.queue.remove(min_node)
      self.update_weights(min_node)
      if min_node == self.sfin: break
      if self.height_matrix[min_node[0]][min_node[1]] == 0 and not self.part1: # For part 2
        self.sfin = min_node
        break
      if len(self.queue) == 0: return float('inf')

    min_path = self.find_min_path()
    return self.path_size(min_path)
  
  # Compute all neighbours of node, where we can go from node
  def neighbours(self, node):
    pos_i = node[0]
    pos_j = node[1]
    out = []
    for i in [-1, 0, 1]:
      for j in [-1, 0, 1]:
        if abs(i) == 1 and abs(j) == 1: continue

        x = pos_i + i
        y = pos_j + j
        if (x == pos_i and y == pos_j) or x < 0 or x > self.m - 1 or y < 0 or y > self.n - 1: continue

        out.append((pos_i + i, pos_j + j))
    return out
  
  def weight_node(self, node):
    return self.weight_matrix[node[0]][node[1]]

  def update_weights(self, last_node):
    neighbours = self.neighbours(last_node)
    for node in neighbours:
      tmp = self.weight_node(last_node) + self.distance(last_node, node)
      if self.weight_node(node) > tmp:
        self.queue.add(node)
        self.weight_matrix[node[0]][node[1]] = tmp
        self.previous_nodes[node[0]][node[1]] = last_node
  
  def find_min_in_queue(self):
    return min(self.queue, key= lambda node: self.weight_node(node))
  
  def find_min_path(self):
    a = []
    s = self.sfin
    while s != self.sdeb:
      a.append(s)
      s = self.previous_nodes[s[0]][s[1]]
    a.append(self.sdeb)
    a.reverse()
    return a
  
  def distance(self, node1, node2):
    if self.part1:
      delta_height = self.height_matrix[node2[0]][node2[1]] - self.height_matrix[node1[0]][node1[1]]
      return (1 if (node2 in self.neighbours(node1) and delta_height <= 1) else float('inf'))
    else:
      delta_height = self.height_matrix[node2[0]][node2[1]] - self.height_matrix[node1[0]][node1[1]]
      return (1 if (node2 in self.neighbours(node1) and delta_height >= -1) else float('inf'))

  def path_size(self, path):
    distance = 0
    node1 = path[0]
    for i in range(1, len(path)):
      node2 = path[i]
      distance += self.distance(node1, node2)
      node1 = node2
    return distance

height_matrix = []
sdeb = None
sfin = None
for i, line in enumerate(lines):
  tmp_height_vector = []
  for j, e in enumerate(line):
    if e == "S":
      tmp_height_vector.append(0)
      sdeb = (i, j)
    elif e == "E":
      tmp_height_vector.append(25)
      sfin = (i, j)
    else:
      tmp_height_vector.append(string.ascii_lowercase.index(e))
  height_matrix.append(tmp_height_vector)


graph_part1 = Graph(height_matrix, sdeb, sfin)
nbr_steps = graph_part1.run_dijkstra()
print("SOLUTION PART 1:")
print(nbr_steps)

graph_part2 = Graph(height_matrix, sfin, (-1,-1), False)
nbr_steps = graph_part2.run_dijkstra()
print("SOLUTION PART 2:")
print(nbr_steps)
