with open('./input.txt') as f:
  lines = list(map(lambda line: list(map(lambda e: list(map(lambda c: int(c), e.split(","))),line.replace("\n", "").split(" -> "))),f.readlines()))

part = 1 # Variable: part = i => part i of exercise

# Find min and max x
min_x = lines[0][0][0]
max_x = lines[0][0][0]
min_y = lines[0][0][1]
max_y = lines[0][0][1]
for paths in lines:
  for path in paths:
    x = path[0]
    y = path[1]
    if x < min_x: min_x = x
    if x > max_x: max_x = x
    if y < min_y: min_y = y
    if y > max_y: max_y = y

if part == 2:
  # Not optimal: I took 800 arbitrarily so that the base is wide enough
  min_x = -800
  max_x = 800

def transform_node(node):
  return [node[0] - min_x + 1, node[1]]

lines = list(map(lambda line: list(map(lambda node:  transform_node(node), line)), lines))
source = [501 - min_x, 0]

# Draw cave

class Cave:
  def __init__(self, lines, min_y, max_y, max_x, source, part):
    self.source = source
    self.min_y = min_y
    self.max_y = max_y
    self.max_x = max_x
    self.width = max_x - min_x + 3
    self.depth = max_y + 2 if part == 1 else max_y + 3
    self.check_part1 = False
    self.check_part2 = False
    self.matrix = [["." for _j in range(self.width)] for _i in range(self.depth)]
    self.set_matrix(source[0], source[1], "+")
    for paths in lines:
      for i in range(len(paths) - 1):
        self.draw_path(paths[i], paths[i + 1])
    
    # Last line (if part 2)
    if part == 2: self.draw_path([0, self.depth - 1], [self.width - 1, self.depth - 1])

  def get_matrix(self, x, y):
    return self.matrix[y][x]
  
  def set_matrix(self, x, y, value):
    self.matrix[y][x] = value
  
  def draw_path(self, node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    if x1 == x2:
      r = range(y1, y2 + 1) if y2 >= y1 else range(y1, y2 - 1, -1)
      for i in r:
        self.set_matrix(x1, i, "#")
    else:
      r = range(x1, x2 + 1) if x2 >= x1 else range(x1, x2 - 1, -1)
      for i in r:
        self.set_matrix(i, y1, "#")
  
  def sand_in_rest(self, x, y):
    return (self.get_matrix(x - 1, y + 1) != "." and self.get_matrix(x, y + 1) != "." and self.get_matrix(x + 1, y + 1) != ".")
  
  def flowing_to_abyss(self, y):
    self.check_part1 = y + 1 >= self.depth
    return self.check_part1
  
  def fall_step(self, x, y):
    if self.get_matrix(x, y + 1) == ".":
      self.set_matrix(x, y, ".")
      self.set_matrix(x, y + 1, "o")
      return [x, y + 1]
    if self.get_matrix(x - 1, y + 1) == ".":
      self.set_matrix(x, y, ".")
      self.set_matrix(x - 1, y + 1, "o")
      return [x - 1, y + 1]
    if self.get_matrix(x + 1, y + 1) == ".":
      self.set_matrix(x, y, ".")
      self.set_matrix(x + 1, y + 1, "o")
      return [x + 1, y + 1]
    else:
      raise "NOT POSSIBLE"
  
  def produce_new_sand(self):
    sand = self.source
    if self.sand_in_rest(self.source[0], self.source[1]):
        self.check_part2 = True
        return
    while True:   
      if self.flowing_to_abyss(sand[1]) or self.sand_in_rest(sand[0], sand[1]):
        break
      sand = self.fall_step(sand[0], sand[1])


c = Cave(lines, min_y, max_y, max_x, source, part)
count = 0
check = False
while not check:
  c.produce_new_sand()
  count += 1
  check = c.check_part2 if part == 2 else c.check_part1

print('SOLUTION PART '+ str(part) + ":" )
print(count - 1 if part == 1 else count)
