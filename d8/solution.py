with open('./input.txt') as f:
  all_trees = list(map(lambda line: [int(x) for x in line.replace("\n", "")], f.readlines()))

class Tree:
  def __init__(self, i, j, size):
    self.i = i
    self.j = j
    self.size = size

class Grid:
  def __init__(self, all_trees):
    self.m = len(all_trees)
    self.n = len(all_trees[0])
    trees = []
    for i in range(self.m):
      line = []
      for j in range(self.n):
        line.append(Tree(i, j, all_trees[i][j]))
      trees.append(line)
    self.trees = trees
  
  def is_visible_and_score(self, x, y):
    if x in [0, self.m - 1] or y in [0, self.n - 1]:
      return {"is_visible": True, "score": 0}
    size_to_check = self.get_tree(x, y).size
    direction_ranges = [[range(x-1, -1, -1), [y]], [range(x+1, self.m, 1), [y]], [[x], range(y-1, -1, -1)], [[x], range(y+1, self.n, 1)]]
    check = []
    score = 1
    for current_range in direction_ranges:
      score_current_direction = 0
      break_loop = False
      for i in current_range[0]:
        for j in current_range[1]:
          score_current_direction += 1
          if self.get_tree(i,j).size >= size_to_check:
            break_loop = True
            break
        if break_loop: break
      if break_loop:
        check.append(False)
        score = score * score_current_direction
        continue
      score = score * score_current_direction
      check.append(True)
    return {"is_visible": sum(check) > 0, "score": score}
  
  def count_visible_trees_and_max_scenic_score(self):
    count = 0
    scores = []
    for i in range(0, self.m):
      for j in range(0, self.n):
        result = self.is_visible_and_score(i, j)
        count = count + 1 if result["is_visible"] else count
        scores.append(result["score"])
    return {"visible_trees": count, "max_scenic_score": max(scores)}

  def get_tree(self, i, j):
    return self.trees[i][j]


solutions = Grid(all_trees).count_visible_trees_and_max_scenic_score()

print("SOLUTION PART 1:")
print(solutions["visible_trees"])

print("SOLUTION PART 2:")
print(solutions["max_scenic_score"])