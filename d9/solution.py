import math

with open('./input.txt') as f:
    lines = list(map(lambda line: line.split(), list(map(lambda line: line.replace("\n", ""),f.readlines()))))

def distance(p0, p1):
  return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def touch(p0, p1):
  return distance(p0, p1) <= math.sqrt(2)

def count_visited_knots_by_tail(rope_length):
  all_knots = [(0,0)] * rope_length
  tail_visited_nodes = {(0,0)}
  DIRECTIONS = {
    "R": [1, 0],
    "U": [0, 1],
    "L": [-1, 0],
    "D": [0, -1]
  }
  for line in lines:
    dir, steps = line
    direction_vector = DIRECTIONS[dir]
    for i in range(1, int(steps) + 1):
      # Move the head knot
      x, y = all_knots[0]
      all_knots[0] = (x + direction_vector[0], y + direction_vector[1])

      # Then move others knots
      for idx_knot in range(1, rope_length):
        followed_knot  = all_knots[idx_knot - 1]
        following_knot = all_knots[idx_knot]
        if touch(following_knot, followed_knot):
          continue
        else:
          # The following knot has to move
          x_following, y_following = following_knot
          x_followed, y_followed = followed_knot
          delta_x_following = min([1, x_followed - x_following]) if x_followed > x_following else max([-1, x_followed - x_following])
          delta_y_following = min([1, y_followed - y_following]) if y_followed > y_following else max([-1, y_followed - y_following])
          all_knots[idx_knot] = (x_following + delta_x_following, y_following + delta_y_following)

      tail_visited_nodes.add(all_knots[rope_length - 1])

  return len(tail_visited_nodes)

print("SOLUTION PART 1:")
print(count_visited_knots_by_tail(2))

print("SOLUTION PART 2:")
print(count_visited_knots_by_tail(10))
