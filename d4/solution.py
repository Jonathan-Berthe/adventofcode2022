with open('./input.txt') as f:
  pairs = list(map(lambda line: list(map(lambda elem: list(map(lambda x: int(x),elem.split('-'))),line.split(","))),map(lambda line: line.replace("\n", ""),f.readlines())))
  # => pair i of pairs represent a pair of Elves, and looks like [v1, v2] with v a vector [x, y] which represent a section going from x to y

class Section:
  def __init__(self, vector):
    self.x = vector[0]
    self.y = vector[1]
  
  def is_fully_contains(self, other_section):
    return (self.x >= other_section.x and self.y <= other_section.y)

  def overlap(self, other_section):
    # will overlap if ||self|| + ||other_section|| >= ||[min(x1,x2), max(y1, y2)]||
    return (self.y - self.x) + (other_section.y - other_section.x) >= max(self.y, other_section.y) - min(self.x, other_section.x)

count_part1 = 0
count_part2 = 0
for pair in pairs:
  s1 = Section(pair[0])
  s2 = Section(pair[1])
  if s1.is_fully_contains(s2) or s2.is_fully_contains(s1):
    count_part1 += 1
  if s1.overlap(s2):
    count_part2 += 1

print("SOLUTION PART 1:")
print(count_part1)

print("SOLUTION PART 2:")
print(count_part2)
