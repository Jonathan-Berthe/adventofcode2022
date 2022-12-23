## Helper classes and methods
def sum_lists(v1, v2):
  out = []
  for i, x in enumerate(v1):
    out.append(x + v2[i])
  return out

class Elve:
  def __init__(self, initial_pos):
    self.pos = initial_pos
    self.proposed_pos = None
  
  def neighbourgs(self):
    x, y = self.pos
    out = []
    for i in [-1, 0, 1]:
      for j in [-1, 0, 1]:
        if i == 0 and j == 0:
          continue
        out.append((x + i, y + j))
    return out

class Diffusion:
  def __init__(self, elves):
    self.elves = elves
    self.directions = [(-1,0), (1,0), (0,-1), (0,1)]
    self.counter = 0
  
  def run(self, n):
    for _i in range(n):
      self.counter += 1
      self.round()
  
  def run_part2(self):
    previous_pos = self.all_positions().copy()
    while True:
      self.run(1)
      new_pos = self.all_positions().copy()    
      if len(set(new_pos) - set(previous_pos)) == 0:      
        break
      previous_pos = new_pos
    return self.counter
  
  def all_positions(self):
    return list(map(lambda e: e.pos, self.elves))
  
  def all_proposed_positions(self):
    return list(map(lambda e: e.proposed_pos, self.elves))
  
  def area(self):
    all_x = list(map(lambda e: e[0], self.all_positions()))
    all_y = list(map(lambda e: e[1], self.all_positions()))
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)
    return abs((max_x - min_x + 1)) * abs((max_y - min_y + 1)) - len(self.elves)
  
  def round(self):
    elves_with_proposal = []
    all_proposal = []
    all_proposal_arleady_excluded = []
    for elve in elves:
      neighbourgs = elve.neighbourgs()
      all_elves_pos = self.all_positions()
      check = True
      for neighbourg in neighbourgs:
        if neighbourg in all_elves_pos:
          check = False
          break
      if check:
        continue
      for dir in self.directions:
        if self.check_direction(elve, dir, all_elves_pos):
          proposal = tuple(sum_lists(list(elve.pos), dir))
          if proposal in all_proposal_arleady_excluded:
            break
          if proposal in all_proposal:
            elve_to_remove = elves_with_proposal[all_proposal.index(proposal)]
            elve_to_remove.proposed_pos = None
            elves_with_proposal.remove(elve_to_remove)
            all_proposal.remove(proposal)
            all_proposal_arleady_excluded.append(proposal)
            break
          elve.proposed_pos = proposal
          elves_with_proposal.append(elve)
          all_proposal.append(proposal)
          break

    for elve in elves_with_proposal:
      elve.pos = elve.proposed_pos
      elve.proposed_pos = None
    pop_dir = self.directions.pop(0)
    self.directions.append(pop_dir)

  def check_direction(self, elve, dir, all_elves_pos):
    tmp = sum_lists(list(elve.pos), dir)
    for i in range(-1,2):
      tmp2 = tmp.copy()
      tmp2[dir.index(0)] = tmp[dir.index(0)] + i
      if tuple(tmp2) in all_elves_pos:
        return False
    return True 

## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""), f.readlines()))

elves = set()
for i, line in enumerate(lines):
  for j in range(len(line)):
    if line[j] == "#":
      elves.add(Elve((i, j)))

d = Diffusion(elves)
d.run(10)

print("SOLUTION PART 1:")
print(d.area())

print("SOLUTION PART 2:")
print(d.run_part2())
