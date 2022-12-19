import math
from helper_lists import start_list, cycle_list

## Helper methods and classes
class Rock:
  def __init__(self, shape):
    self.shape = shape
    self.reference = shape[0]
    self.is_falling = False
  
  def complete_fall(self, instructions, current_instruction_index, cave):
    self.is_falling = True
    iter_idx = current_instruction_index
    len_instructions = len(instructions)
    while self.is_falling:
      current_instruction = instructions[iter_idx]
      self.gas_move(current_instruction, cave)
      self.fall(cave)
      iter_idx = (iter_idx + 1) % len_instructions
    # Update cave
    cave.current_instruction_index = iter_idx
    previous_height = cave.height
    cave.height = max(previous_height, self.reference[1] + 1)
    delta = cave.height - previous_height
    cave.all_delta_height.append(delta)
    if cave.height > previous_height:
      for _i in range(delta):
        cave.cave_matrix.append(["." for _j in range(cave.width)])
    for point in self.shape:
      cave.set_point(point[0], point[1], "#")
  
  def gas_move(self, direction, cave):
    if direction == ">" and not self.is_blocked_on_side(cave, False):
      for point in self.shape:
        point[0] += 1
    elif direction == "<" and not self.is_blocked_on_side(cave, True):
      for point in self.shape:
        point[0] -= 1
  
  def fall(self, cave):
    if not self.is_blocked_on_floor(cave):
      for point in self.shape:
        point[1] -= 1

  def is_blocked_on_side(self, cave, left = True):
    for point in self.shape:
      if (point[0] == 0 or cave.get_point(point[0] - 1, point[1]) == "#") and left:
        return True
      if (point[0] == 6 or cave.get_point(point[0] + 1, point[1]) == "#") and not left:
        return True
    return False
  
  def is_blocked_on_floor(self, cave):
    for point in self.shape:
      if point[1] == 0 or cave.get_point(point[0], point[1] - 1) == "#":
        self.is_falling = False
        return True
    return False

class HorizontalLine(Rock):
  def __init__(self, reference):
    shape = [reference]
    for i in range(1, 4):
      new_point = [reference[0] + i, reference[1]]
      shape.append(new_point)
    super().__init__(shape)

class VerticalLine(Rock):
  def __init__(self, reference):
    shape = [reference]
    for i in range(1, 4):
      new_point = [reference[0], reference[1] - i]
      shape.append(new_point)
    super().__init__(shape)

class Cross(Rock):
  def __init__(self, reference):
    shape = [reference]
    for i in range(-1, 2):
      new_point = [reference[0] + i, reference[1] - 1]
      shape.append(new_point)
    shape.append([reference[0], reference[1] - 2])
    super().__init__(shape)

class Square(Rock):
  def __init__(self, reference):
    shape = [reference, [reference[0] + 1, reference[1]], [reference[0], reference[1] - 1], [reference[0] + 1, reference[1] - 1]]
    super().__init__(shape)

class InverseL(Rock):
  def __init__(self, reference):
    shape = [reference]
    shape.append([reference[0], reference[1] - 1])
    for i in range(-2, 1):
      new_point = [reference[0] + i, reference[1] - 2]
      shape.append(new_point)
    super().__init__(shape)
  
class Cave:
  def __init__(self, flow_instructions, init_height = 0, width = 7):
    self.height = init_height
    self.width = width
    self.flow_instructions = flow_instructions
    self.cave_matrix = [["." for _j in range(self.width)] for _i in range(self.height + 7)]
    self.current_falling_rock = None
    self.current_instruction_index = 0
    self.all_delta_height = []

  def print_cave(self):
    arr = [[0 for _j in range(len(self.cave_matrix[0]))] for _i in range(len(self.cave_matrix))]
    for i in range(len(self.cave_matrix)):
      arr[i][:] = self.cave_matrix[len(self.cave_matrix) - 1 - i]

  def run(self, nbr_iters):
    ordered_shapes = ["HorizontalLine", "Cross", "InverseL", "VerticalLine", "Square"]
    iter_idx = 0
    count = 0
    while count < nbr_iters:
      current_rock = ordered_shapes[iter_idx]
      self.pop_new_rock(current_rock)
      iter_idx = (iter_idx + 1) % len(ordered_shapes)
      for i in range(self.width):
        if self.cave_matrix[self.height][i] != "#":
          break
      count += 1

  def pop_new_rock(self, rock_type):
    # Instanciate new rock at correct position
    if rock_type == "HorizontalLine":
      reference = [2, self.height + 3]
      self.current_falling_rock = HorizontalLine(reference)
    elif rock_type == "VerticalLine":
      reference = [2, self.height + 6]
      self.current_falling_rock = VerticalLine(reference)
    elif rock_type == "Cross":
      reference = [3, self.height + 5]
      self.current_falling_rock = Cross(reference)
    elif rock_type == "Square":
      reference = [2, self.height + 4]
      self.current_falling_rock = Square(reference)
    elif rock_type == "InverseL":
      reference = [4, self.height + 5]
      self.current_falling_rock = InverseL(reference)
    # Now rock can fall
    self.current_falling_rock.complete_fall(self.flow_instructions, self.current_instruction_index, self)
    self.current_falling_rock = None
  
  def get_point(self, x, y):
    return self.cave_matrix[y][x]
  
  def set_point(self, x, y, value):
    self.cave_matrix[y][x] = value


## Parse input
with open('./input.txt') as f:
  lines = f.readlines()
gas_movements = lines[0]

## Original code for Part 1 - Also used to manually deduce start_list and cycle_list from all_delta_height for Part 2

# c = Cave(gas_movements)
# c.run(2022)
# print(c.height)
# print(c.all_delta_height)

## Part 2 resolution (Partially manual aha)

# If we are able to find the height after 1000000000000 rocks have stopped, that means there is a trick.
# Hypothesis: from a certain moment, there will be a cycle which appears in the iterations.
# => I printed in my terminal all_delta_height (with all_delta_height[i] = increase of height between rock i and (i + 1)) for 10000 rocks. After that I selected some sequences of printed list (in a trial-error way) and then I cmd+F these to see if it was repeating. Very easily and quickly, it allowed me to find start_list and cycle_list so that we have all_delta_height = [*start_list, *cycle_list, *cycle_list, *cycle_list, ....]
# From that, we can find height for n rock with: height = sum(start_list) + (math.floor(n - len(start_list) / len(cycle_list))) * sum(cycle_list) + sum(cycle_list[0 : (num_iter - len(start_list)) % len_cycle_list])

def compute_height(num_iter):
  total_height = 0
  len_cycle_list = len(cycle_list)
  sum_cycle_list = sum(cycle_list)
  sum_start_list = sum(start_list)
  if num_iter <= len(start_list):
    total_height = sum(start_list[0:num_iter])
  else:
    total_height = sum_start_list + (math.floor((num_iter - len(start_list)) / len_cycle_list)) * sum_cycle_list + sum(cycle_list[0 : (num_iter - len(start_list)) % len_cycle_list])
  return total_height

print("SOLUTION PART 1:")
num_iter_part1 = 2022
print(compute_height(num_iter_part1))

print("SOLUTION PART 2:")
num_iter_part2 = 1000000000000
print(compute_height(num_iter_part2))
