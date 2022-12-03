import string

with open('./input.txt') as f:
    lines = list(map(lambda line: line.replace("\n", ""),f.readlines()))

class Rucksack:
  def __init__(self, all_items_str):
    number_of_items = len(all_items_str)
    self.all_items_str = all_items_str
    self.first_compartment  = all_items_str[:number_of_items//2]
    self.second_compartment = all_items_str[number_of_items//2:]
  
  def shared_item_between_compartment(self):
    # See https://bobbyhadz.com/blog/python-find-common-characters-between-two-strings
    return ''.join(
      set(self.first_compartment).intersection(self.second_compartment)
    )
  
  def shared_item_with_other_rucksacks(self, rucksack1, rucksack2):
    return ''.join(
      set(self.all_items_str).intersection(rucksack1.all_items_str).intersection(rucksack2.all_items_str)
    )
  
  @staticmethod
  def get_item_priority(item):
    is_upper = item.isupper()
    return 27 + string.ascii_uppercase.index(item) if is_upper else 1 + string.ascii_lowercase.index(item)

all_rucksacks = list(map(lambda line: Rucksack(line), lines))

print("SOLUTION PART 1:")
print(sum(list(map(lambda rucksack: Rucksack.get_item_priority(rucksack.shared_item_between_compartment()), all_rucksacks))))

print("SOLUTION PART 2:")
total_prio = 0
for i in range(0, len(all_rucksacks), 3):
  total_prio += Rucksack.get_item_priority(all_rucksacks[i].shared_item_with_other_rucksacks(all_rucksacks[i + 1], all_rucksacks[i + 2]))
print(total_prio)
