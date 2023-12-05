import ast

class Blizzard:
  def __init__(self, pos, dir):
    self.pos = pos
    self.dir = dir

class MapState:
  def __init__(self, init_state, len_path_boundary):
    self.state = init_state
    self.width = len(init_state[0])
    self.height = len(init_state)
    all_bliz = set()
    for i in range(self.height):
      for j in range(self.width):
        tmp = self.state[i][j]
        if tmp in ["<", "^", ">", "v"]:
          all_bliz.add(Blizzard((i, j), tmp))
    self.blizzards = all_bliz
    self.init_string_state = self.to_string()
    self.all_possible_cyclic_str = [self.init_string_state]
    self.len_path_boundary = len_path_boundary 
    self.find_all_possible_cyclic_str()
    self.period = len(self.all_possible_cyclic_str)
    self.reset_exploration()

  def next_possible_pos(self, state, current_pos):
    possible_pos = []
    for i in [-1, 0, 1]:
      for j in [-1, 0, 1]:
        if current_pos[0] + i < 0 or current_pos[0] + i > self.height - 1:
          continue
        if abs(i) == 1 and abs(j) == 1:
          continue
        candidate_i = current_pos[0] + i
        candidate_j = current_pos[1] + j
        if state[candidate_i][candidate_j] == ".":
          possible_pos.append((candidate_i, candidate_j))
    return possible_pos

  def find_all_possible_cyclic_str(self):
    tmp = self.to_string()
    while True:
      self.blizzard_step()
      tmp = self.to_string()
      if tmp == self.init_string_state:
        break
      self.all_possible_cyclic_str.append(tmp)

  def blizzard_step(self):
    for blizzard in self.blizzards:
      i = blizzard.pos[0]
      j = blizzard.pos[1]
      self.state[i][j] = self.state[i][j].replace(blizzard.dir,"", 1)
      if len(self.state[i][j]) == 0:
        self.state[i][j] = "."
      if blizzard.dir == "v":
        blizzard.pos = (i + 1, j) if i + 2 < self.height else (1, j)
      elif blizzard.dir == ">":
        blizzard.pos = (i, j + 1) if j + 2 < self.width else (i, 1)
      elif blizzard.dir == "^":
        blizzard.pos = (i - 1, j) if i > 1 else (self.height - 2, j)
      elif blizzard.dir == "<":
        blizzard.pos = (i, j - 1) if j > 1 else (i, self.width - 2)
      i_new = blizzard.pos[0]
      j_new = blizzard.pos[1]
      self.state[i_new][j_new] = self.state[i_new][j_new].replace(".","")
      self.state[i_new][j_new] = ''.join(sorted(self.state[i_new][j_new] + blizzard.dir))
 
  def to_string(self):
    return str(self.state)

  def key(self, pos, time):
    return f"({pos[0]}, {pos[1]}, {time})"

  def reset_exploration(self, boundary_factor = 1):
    self.memoized_steps = {}
    self.min_steps = self.len_path_boundary * boundary_factor
    self.found_sol = False
    self.memoized_steps = {}

  def explore_all_paths(self, current_pos = (0, 1), time = 0, previous_pos = [], onward = True):
    key = self.key(current_pos, time)
    if key in self.memoized_steps:
      return self.memoized_steps[key]
    # Prune rules
    if time > self.min_steps:
      self.memoized_steps[key] = float('inf')
      return float('inf')
    previous_indices = [i for i, x in enumerate(previous_pos) if x == current_pos]
    for indice in previous_indices:
      if (time % self.period == indice % self.period) and indice != time:
        self.memoized_steps[key] = float('inf')
        return float('inf')
    # Check if target point is reached
    state = ast.literal_eval(self.all_possible_cyclic_str[time % self.period])
    if (onward and current_pos[0] == self.height - 1 and current_pos[1] == self.width - 2) or (not onward and current_pos[0] == 0 and current_pos[1] == 1):
      self.min_steps = min(time, self.min_steps)
      self.memoized_steps[self.key(current_pos, time)] = time
      self.found_sol = True
      return time
    # Call method recursively over all next possible current positions
    tmp = []
    all_possibilities = self.next_possible_pos(state, current_pos)
    for new_pos in all_possibilities:
      new_previous_pos = previous_pos.copy()
      new_previous_pos.append(new_pos)
      tmp.append(self.explore_all_paths(new_pos, time + 1, new_previous_pos, onward))
    min_steps = min(tmp) if len(tmp) > 0 else float('inf')
    self.memoized_steps[key] = min_steps
    return min_steps

## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: list(line.replace("\n", "")), f.readlines()))
dict = {}

## Resolution
len_path_boundary = 350 # 30 for dummy_input.txt
m = MapState(lines, len_path_boundary)

m.explore_all_paths()
journey1 = m.min_steps - 1
print("SOLUTION PART 1:")
print(journey1)

m.reset_exploration(2)
m.explore_all_paths((m.height - 1, m.width - 2), journey1 + 1, [], False)
journey2 = m.min_steps - journey1 - 1

m.reset_exploration(3)
m.explore_all_paths((0, 1), journey1 + journey2 + 1, [])
journey3 = m.min_steps - journey1 - journey2 - 1

print("SOLUTION PART 2:")
print(journey1 + journey2 + journey3)
