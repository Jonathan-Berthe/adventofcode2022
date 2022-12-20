## Helper methods
def intersection(a, b):
  return set(a).intersection(b)

# Return set with all 6 sides of cube (cube of type [x, y, z]).
# A side correspond to a tuple (a,b,c) in wich one element is an integer and others are lists.
# Exemple: ((3, 4), 2, (6, 8))
# => Side with y = 2, x in [3, 4], z in [6, 8]
def sides_of_cube(cube):
  sides = []
  for i in range(3):
    for j in range(2):
      side = [None, None, None]
      side[i] = cube[i] + j
      for k in list(set([0,1,2]) - set([i])):
        side[k] = (cube[k], cube[k] + 1)
      sides.append(tuple(side))
  return set(sides)

## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: list(map(lambda e: int(e), line.replace("\n", "").split(","))),f.readlines()))

## Part 1
all_free_sides = sides_of_cube(lines[0])
single_points = set()
for i in range(1, len(lines)):
  cube = lines[i]
  new_sides = sides_of_cube(cube)
  inter_sides = intersection(all_free_sides, new_sides)
  all_free_sides = all_free_sides.union(new_sides) - inter_sides

print("SOLUTION PART 1:")
print(len(all_free_sides))

## Part 2 (with flood fill algo)

def flood_fill(cube_init, lines):
  already_visited = set()
  count = 0
  queue = [cube_init]
  while len(queue) > 0:
    x, y, z = queue.pop(0)
    if (x, y, z) not in already_visited:
      already_visited.add((x, y, z))
      for x_next, y_next, z_next in ((x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)):
        if -1 <= x_next <= 22 and -1 <= y_next <= 22 and -1 <= z_next <= 22:
          if [x_next, y_next, z_next] in lines:
            count += 1
          else:
            queue.append((x_next, y_next, z_next))
  return count

surface_part2 = flood_fill((0,0,0), lines)

print("SOLUTION PART 2:")
print(surface_part2)
