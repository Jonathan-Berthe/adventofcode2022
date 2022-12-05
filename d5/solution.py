with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""),f.readlines()))

class Crate:
  def __init__(self, letter, x, y):
    self.letter = letter
    self.x = x
    self.y = y

  def set_new_position(self, x, y):
    self.x = x
    self.y = y


class Cargo:
  def __init__(self, crates, instructions):
    self.crates = crates
    self.instructions = instructions
    self.height = self.find_max_height()
  
  # part = i => part i of exercise
  def run(self, part):
    for instruction in self.instructions:
      if part == 1:
        self.perform_instruction_p1(instruction)
      else:
        self.perform_instruction_p2(instruction)
  
  def perform_instruction_p1(self, instruction):
    for _ in range(instruction[0]):
      crate_to_move = self.crate_on_top_of_stack(instruction[1] - 1)
      new_postion_x = instruction[2] - 1
      new_position_y = self.find_min_y_of_stack(new_postion_x) - 1
      crate_to_move.set_new_position(new_postion_x, new_position_y)
  
  def perform_instruction_p2(self, instruction):
    new_postion_x = instruction[2] - 1
    new_position_y_base = self.find_min_y_of_stack(new_postion_x) - 1
    for i in range(instruction[0]):
      crate_to_move = self.crate_on_top_of_stack(instruction[1] - 1)
      crate_to_move.set_new_position(new_postion_x, new_position_y_base - (instruction[0] - i) - 1)
  
  def find_min_y_of_stack(self, x):
    stack = list(filter(lambda crate: crate.x == x, self.crates))
    if len(stack) == 0:
      return self.height
    out = stack[0].y
    for crate in stack:
      if crate.y < out:
        out = crate.y
    return out
  
  def crate_on_top_of_stack(self, x):
    stack = list(filter(lambda crate: crate.x == x, self.crates))
    if len(stack) == 0:
      return None
    out = stack[0]
    for crate in stack:
      if crate.y < out.y:
        out = crate
    return out
  
  def find_max_height(self):
    out = self.crates[0].y
    for crate in self.crates:
      if crate.y > out:
        out = crate.y
    return out

steps = []
crates = []
for line_idx, line in enumerate(lines):
  if line.startswith("move"):
    elems = line.split(" ")
    steps.append([int(elems[1]), int(elems[3]), int(elems[5])])
  elif len(line) != 0 and line[1] != "1":
    for c_idx, c in enumerate(line):
      if c.isalnum():
        crates.append(Crate(c, int((c_idx - 1)/4), line_idx))

part = 2 # Variable: part = i => part i of exercise
cargo = Cargo(crates, steps)
cargo.run(part)
solution = ""
for i in range(100): # 100 to be sure we don't miss a stack aha ^^
  skip = False
  if cargo.crate_on_top_of_stack(i-1) is None:
      skip = True
  if not skip:
    solution += cargo.crate_on_top_of_stack(i-1).letter

print('SOLUTION PART '+ str(part) + ":" )
print(solution)