from copy import deepcopy

class Stock:
  def __init__(self, ore = 0, clay = 0, obsidian = 0, geode = 0, ore_robot = 1, clay_robot = 0, obsidian_robot = 0, geode_robot = 0):
    self.ore = ore
    self.clay = clay
    self.obsidian = obsidian
    self.geode = geode
    self.ore_robot = ore_robot
    self.clay_robot = clay_robot
    self.obsidian_robot = obsidian_robot
    self.geode_robot = geode_robot

  def key(self, minute):
    return f"{minute} {self.ore} {self.clay} {self.obsidian} {self.geode} {self.ore_robot} {self.clay_robot} {self.obsidian_robot} {self.geode_robot}"
  
class Blueprint:
  def __init__(self, id, ore_cost, clay_cost, obsidian_cost, geode_cost, part2 = True):
    self.id = id
    self.ore_cost = ore_cost
    self.clay_cost = clay_cost
    self.obsidian_cost = obsidian_cost
    self.geode_cost = geode_cost
    self.max_geode = 0
    self.part2 = part2
    self.total_minutes = 32 if part2 else 24
    self.min_time_with_geode_robot = self.total_minutes
    self.memoized_max_geodes = {}

  def iterate(self, stock, minute = 1):
    key = stock.key(minute)
    if key in self.memoized_max_geodes:
      return self.memoized_max_geodes[key]

    # Prune if there is no possible way to reach the current max
    nbr_geode_robot = stock.geode_robot
    theorical_max = stock.geode
    for i in range(minute, self.total_minutes + 1):
      nbr_geode_robot += 1
      theorical_max += nbr_geode_robot
    if theorical_max <= self.max_geode:
      self.memoized_max_geodes[key] = -1
      return -1
    
    # Prune if we already had a better scenario
    if (minute >= self.min_time_with_geode_robot + 1 and stock.geode_robot == 0):
      self.memoized_max_geodes[key] = -1
      return -1
    
    # Prune rule for part 1
    if not self.part2 and ((minute >= 9 and stock.clay_robot < 1) or (minute >= 17 and stock.obsidian_robot < 1)):
      self.memoized_max_geodes[key] = -1
      return -1

    # Prune rule for part 2
    if self.part2 and (minute >= 15 and stock.clay_robot < 4):
      self.memoized_max_geodes[key] = -1
      return -1

    if minute == self.total_minutes + 1:
      self.max_geode = max(self.max_geode, stock.geode)
      self.memoized_max_geodes[key] = stock.geode_robot
      return stock.geode_robot

    all_possibilities = []
    possible_robots = self.possible_robots_to_build(stock, minute)
    for robot in possible_robots:
      new_stock = deepcopy(stock)
      self.collect_ressource(new_stock)
      self.build_robot(robot, new_stock, minute)        
      all_possibilities.append(self.iterate(new_stock, minute + 1))

    self.collect_ressource(stock)
    all_possibilities.append(self.iterate(stock, minute + 1))
    max_value = max(all_possibilities)
    self.memoized_max_geodes[key] = max_value
    return max_value
  
  def possible_robots_to_build(self, stock, minute):
    out = []
    if stock.ore >= self.geode_cost[0] and stock.obsidian >= self.geode_cost[1]:
      return ["GEODE"] # Ignore others robots if it's possible to build GEODE
    if stock.ore >= self.ore_cost and stock.ore_robot <= max(self.ore_cost, self.clay_cost, self.obsidian_cost[0], self.geode_cost[0]) and ((self.part2 and minute < 15) or (not self.part2 and minute < 11)):
      out.append("ORE")
    if stock.ore >= self.clay_cost and stock.clay_robot <= self.obsidian_cost[1] and ((self.part2 and minute < 25) or (not self.part2 and minute < 20)):
      out.append("CLAY")
    if stock.ore >= self.obsidian_cost[0] and stock.clay >= self.obsidian_cost[1] and stock.obsidian_robot <= self.geode_cost[1] and ((self.part2 and minute < 30) or (not self.part2 and minute < 24)):
      out.append("OBSIDIAN")
    return out
  
  def build_robot(self, type, stock, minute):
    if type == "ORE":
      stock.ore -= self.ore_cost
      stock.ore_robot += 1
    elif type == "CLAY":
      stock.ore -= self.clay_cost
      stock.clay_robot += 1
    elif type == "OBSIDIAN":
      stock.ore -= self.obsidian_cost[0]
      stock.clay -= self.obsidian_cost[1]
      stock.obsidian_robot += 1
    elif type == "GEODE":
      stock.ore -= self.geode_cost[0]
      stock.obsidian -= self.geode_cost[1]
      stock.geode_robot += 1
      self.min_time_with_geode_robot = min(minute, self.min_time_with_geode_robot)
  
  def collect_ressource(self, stock):
    stock.ore += stock.ore_robot
    stock.clay += stock.clay_robot
    stock.obsidian += stock.obsidian_robot
    stock.geode += stock.geode_robot

with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""), f.readlines()))

import time
start = time.time()
part = 2 # Variable: part = i => part i of exercise

blueprints = []
for line in lines:
  tmp = line.split(": ")
  id = tmp[0].split(" ")[1]
  costs_str = tmp[1].split(".")
  ore_cost = int(costs_str[0].split(" ")[4])
  clay_cost = int(costs_str[1].split(" ")[5])
  obsidian_cost = [int(costs_str[2].split(" ")[5]), int(costs_str[2].split(" ")[8])]
  geode_cost = [int(costs_str[3].split(" ")[5]), int(costs_str[3].split(" ")[8])]
  blueprints.append(Blueprint(id, ore_cost, clay_cost, obsidian_cost, geode_cost, part == 2))
  if len(blueprints) == 3 and part == 2:
    break

sum = 0
prod = 1
for blueprint in blueprints:
  blueprint.iterate(Stock())
  prod = prod * blueprint.max_geode
  sum += blueprint.max_geode * int(blueprint.id)

print('SOLUTION PART '+ str(part) + ":" )
if part == 1:
  print(sum)
else:
  print(prod)

end = time.time()
print(end - start)
