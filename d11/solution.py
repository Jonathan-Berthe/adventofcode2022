import math
import heapq
import numpy

with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""),f.readlines()))

class Monkey:
  def __init__(self, init_items, operation, test_divider, monkey_to_throw_true, monkey_to_throw_false):
    self.items = init_items
    self.operation = operation
    self.test_divider = test_divider
    self.monkey_to_throw_true = monkey_to_throw_true
    self.monkey_to_throw_false = monkey_to_throw_false
    self.inspected_items = 0
  
  def add_item(self, item):
    self.items.append(item)
  
  def inspect_items(self, all_monkeys, worry_level_divider, reducer_divider):
    while len(self.items) > 0:
      old = self.items.pop(0)
      new_worry_level = math.floor(eval(self.operation) / worry_level_divider) % reducer_divider
      check = (new_worry_level % self.test_divider == 0)
      if check:
        all_monkeys[self.monkey_to_throw_true].add_item(new_worry_level)
      else:
        all_monkeys[self.monkey_to_throw_false].add_item(new_worry_level)
      self.inspected_items += 1

def perform_round(all_monkeys, worry_level_divider, reducer_divider):
  for x in all_monkeys:
    all_monkeys[x].inspect_items(all_monkeys, worry_level_divider, reducer_divider)

def monkey_business(all_monkeys):
  inspected_items_list = list(map(lambda monkey: all_monkeys[monkey].inspected_items, all_monkeys))
  return numpy.prod(list(heapq.nlargest(2, inspected_items_list)))

def solution(is_part_1, all_monkeys):
  worry_level_divider = 3 if is_part_1 else 1
  nbr_round = 20 if is_part_1 else 10000
  reducer_divider = numpy.prod(list(map(lambda monkey: all_monkeys[monkey].test_divider, all_monkeys)))
  for _i in range(nbr_round):
    perform_round(all_monkeys, worry_level_divider, reducer_divider)
  return monkey_business(all_monkeys)

# Parse input
incrm = 0
nbr_lines = len(lines)
all_monkeys = {}
while incrm < nbr_lines:
  monkey_name = lines[incrm][7]
  init_items = list(map(lambda e: int(e), lines[incrm + 1][18:].split(", ")))
  operation = lines[incrm + 2][19:]
  test_divider = int(lines[incrm + 3][21:])
  monkey_to_throw_true = lines[incrm + 4][29:]
  monkey_to_throw_false = lines[incrm + 5][30:]
  all_monkeys[monkey_name] = Monkey(init_items, operation, test_divider, monkey_to_throw_true, monkey_to_throw_false)
  incrm += 7

# Compute solution
part = 2 # Variable: part = i => part i of exercise
print('SOLUTION PART '+ str(part) + ":" )
print(solution(part == 1, all_monkeys))
