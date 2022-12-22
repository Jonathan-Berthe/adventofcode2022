import re

## Helper classes and methods
ROTATIONS = [">", "v", "<", "^"]
def reverseindex(lst, value):
  return len(lst) - 1 - lst[::-1].index(value)

def extend_str(str, n):
  for _i in range(n):
    str = str + " "
  return str

class Walk:
  def __init__(self, board, instructions, part2 = False):
    self.board = board
    self.instructions = instructions
    self.instruction_idx = 0
    self.current_facing = ">"
    self.current_pos = (0, self.board.plan[0].index('.'))
    self.part2 = part2
  
  def run(self):
    for instruction in self.instructions:
      self.perform_instruction(instruction)
  
  def find_opposite(self, x, y):
    if self.part2:
      opp = self.board.dict[f"({x}, {y})"]
      self.current_facing = opp[2]
      return (opp[0], opp[1])
    else:
      if self.current_facing == ">":
        return (x, min(self.board.plan[x].index('.'), self.board.plan[x].index('#')))
      if self.current_facing == "<":
        return (x, max(reverseindex(self.board.plan[x], '.'), reverseindex(self.board.plan[x], '#')))
      if self.current_facing == "v":
        col = self.board.get_column(y)
        return (min(col.index('.'), col.index('#')), y)
      if self.current_facing == "^":
        col = self.board.get_column(y)
        return (max(reverseindex(col, "."), reverseindex(col, "#")), y)
  
  def perform_instruction(self, instruction):
    if instruction.isnumeric():     
      self.move_forward(int(instruction))
    else:
      self.rotate(instruction)

  def move_forward(self, count):
    for i in range(count):
      self.move_one_tile()
  
  def move_one_tile(self):
    r, c = self.current_pos
    previous_facing = self.current_facing
    if self.current_facing == ">":
      next_c = (c + 1) % self.board.n
      next_r = r
      if next_c == 0 or self.board.plan[next_r][next_c] == " ":
        next_r, next_c = self.find_opposite(r, c)
    elif self.current_facing == "<":
      next_c = (c - 1) % self.board.n
      next_r = r
      if next_c == self.board.n - 1 or self.board.plan[next_r][next_c] == " ":
        next_r, next_c = self.find_opposite(r, c)
    elif self.current_facing == "v":
      next_r = (r + 1) % self.board.m
      next_c = c
      if next_r == 0 or self.board.plan[next_r][next_c] == " ":
        next_r, next_c = self.find_opposite(r, c)
    elif self.current_facing == "^":
      next_r = (r - 1) % self.board.m
      next_c = c
      if next_r == self.board.m - 1 or self.board.plan[next_r][next_c] == " ":
        next_r, next_c = self.find_opposite(r, c)
    if self.board.plan[next_r][next_c] == "#":
      self.current_facing = previous_facing
      return
    self.current_pos = (next_r, next_c)
  
  def rotate(self, rotation):
    if rotation == "R":
      self.current_facing = ROTATIONS[(ROTATIONS.index(self.current_facing) + 1) % 4]
    else:
      self.current_facing = ROTATIONS[(ROTATIONS.index(self.current_facing) - 1) % 4]
  
  def password(self):
    r, c = self.current_pos
    return 1000 * (r + 1) + 4 * (c + 1) + ROTATIONS.index(self.current_facing)

class Board:
  def __init__(self, plan, max_map_width, dict):
    self.plan = list(map(lambda line: line if max_map_width == len(line) else extend_str(line, max_map_width - len(line)), plan))
    self.m = len(self.plan)
    self.n = len(self.plan[0])
    self.dict = dict
  
  def get_column(self, y):
    col = []
    for i in range(self.m):
      col.append(self.plan[i][y])
    return col

## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""), f.readlines()))

plan = []
intructions = ""
max_map_width = 0
for idx, line in enumerate(lines):
  if line == "":
    instructions = [item for item in re.split('(\d+)', lines[idx + 1]) if item]
    break
  max_map_width = max(max_map_width, len(line))
  plan.append(line)

# Dict to store "opposite" position when we reach borders (for part 2)
dict = {}

# Faces numbering for cube of input.txt:
#
#   |1|2|
#   |3|
# |5|4|
# |6|

# North of 1 <-> South of 6
for i, c in enumerate(range(100,150)):
  dict[f"(0, {c})"] = (199, i, "^")
  dict[f"(199, {i})"] = (0, c, "v")

# East of 1 <-> East of 4
for i, r in enumerate(range(50)):
  dict[f"({r}, 149)"] = (149 - i, 99, "^")
  dict[f"({149 - i}, 99)"] = (r, 149, "<")

# S of 1 <-> E of 3
for i, c in enumerate(range(100,150)):
  dict[f"(49, {c})"] = (50 + i, 99, "<")
  dict[f"({50 + i}, 99)"] = (49, c, "^")

# S of 4 <-> E of 6
for i, c in enumerate(range(50,100)):
  dict[f"(149, {c})"] = (150 + i, 49, "<")
  dict[f"({150 + i}, 49)"] = (149, c, "^")

# E of 6 <-> N of 2
for i, r in enumerate(range(150, 200)):
  dict[f"({r}, 0)"] = (0, 50 + i, "v")
  dict[f"(0, {50 + i})"] = (r, 0, ">")

# E of 5 <-> E of 2
for i, r in enumerate(range(100, 150)):
  dict[f"({r}, 0)"] = (49 - i, 50, ">")
  dict[f"({49 - i}, 50)"] = (r, 0, ">")

# S of 5 <-> E of 3
for i, c in enumerate(range(0, 50)):
  dict[f"(100, {c})"] = (50 + i, 50, ">")
  dict[f"({50 + i}, 50)"] = (100, c, "v")

# Faces numbering for cube of dummy_input.txt:
#
#       |1|
#   |2|3|4|
#       |5|6|

# # N of 1 <-> N of 2
# for i, c in enumerate(range(8,12)):
#   dict[f"(0, {c})"] = (4, 3 - i, "v")
#   dict[f"(4, {3-i})"] = (0, c, "v")
# 
# # W of 1 <-> N of 3
# for i, r in enumerate(range(4)):
#   dict[f"({r}, 8)"] = (4, 4 + i, "v")
#   dict[f"(4, {4 + i})"] = (r, 8, ">")
# 
# # E of 1 <-> E of 6
# for i, r in enumerate(range(4)):
#   dict[f"({r}, 11)"] = (11 - i, 11, "<")
#   dict[f"({11 - i}, 11)"] = (r, 11, "<")
# 
# ###
# # E of 4 <-> N of 6
# for i, r in enumerate(range(4, 8)):
#   dict[f"({r}, 11)"] = (8, 15 - i, "v")
#   dict[f"(8, {15 - i})"] = (r, 11, "<")
# 
# # S of 6 <-> E of 2
# for i, c in enumerate(range(12, 16)):
#   dict[f"(11, {c})"] = (7 - i, 0, ">")
#   dict[f"({7 - i}, 0)"] = (11, c, "^")
# 
# # S of 4 <-> S of 2
# for i, c in enumerate(range(8, 12)):
#   dict[f"(11, {c})"] = (7, 3 - i, "^")
#   dict[f"(7, {3 - i})"] = (11, c, "^")
# 
# # E of 5 <-> S of 3
# for i, r in enumerate(range(8, 12)):
#   dict[f"({r}, 8)"] = (7, 7 - i, "^")
#   dict[f"(7, {7 - i})"] = (r, 8, ">")

print("SOLUTION PART 1:")
board = Board(plan, max_map_width, dict)
w_p1 = Walk(board, instructions)
w_p1.run()
print(w_p1.password())

print("SOLUTION PART 2:")
w_p2 = Walk(board, instructions, True)
w_p2.run()
print(w_p2.password())
