import ast
from functools import cmp_to_key

with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""),f.readlines()))

def compare_lists(list_left, list_right):
  if len(list_left) == 0 and len(list_right) > 0:
    return True
  elif len(list_right) == 0 and len(list_left) > 0:
    return False
  elif len(list_right) == 0 and len(list_right) == 0:
    return None
  left_element = list_left[0]
  right_element = list_right[0]
  check = check_pair_order([[left_element], [right_element]])
  if check is not None: 
    return check
  list_left.pop(0)
  list_right.pop(0)
  return check_pair_order([list_left, list_right])

def check_pair_order(pairs):
  left_packet = pairs[0]
  right_packet =  pairs[1]
  if len(left_packet) == 0 and len(right_packet) > 0:
    return True
  elif len(right_packet) == 0 and len(left_packet) > 0:
    return False
  if left_packet == right_packet:
    return None
  left_element = left_packet[0]
  right_element = right_packet[0]
  check = None
  if isinstance(left_element, int) and isinstance(right_element, int):
    if left_element == right_element:
      check = None
    else:
      return left_element < right_element
  if isinstance(left_element, list) and isinstance(right_element, list):
    check = compare_lists(left_element.copy(), right_element.copy())
  if isinstance(left_element, int) and isinstance(right_element, list):
    check = check_pair_order([[left_element], right_element.copy()])
  if isinstance(left_element, list) and isinstance(right_element, int):
    check = check_pair_order([left_element.copy(), [right_element]])
  if check == None:
    left_packet.pop(0)
    right_packet.pop(0)
    return check_pair_order([left_packet.copy(), right_packet.copy()])
  else:
    return check

current_pairs = []
all_pairs = []
all_pairs_part2 = []
for idx, line in enumerate(lines):
  if len(line) == 0 or idx == len(lines) + 1:
    all_pairs.append(current_pairs)
    current_pairs = []
    continue
  else:
    current_pairs.append(ast.literal_eval(line))
    all_pairs_part2.append(ast.literal_eval(line))
  if idx == len(lines) - 1:
    all_pairs.append(current_pairs)

print("SOLUTION PART 1:")
count = 0
for idx, pairs in enumerate(all_pairs):
  if check_pair_order(pairs):
    count += (idx + 1)
print(count)

print("SOLUTION PART 2:")
# Sort function for part 2
def compare(item1, item2):
  if check_pair_order([item1.copy(), item2.copy()]) is None:
    return 0
  elif check_pair_order([item1.copy(), item2.copy()]):
    return -1
  else:
    return 1

divider1 = [[2]]
divider2 = [[6]]
all_pairs_part2.append(divider1)
all_pairs_part2.append(divider2)
all_pairs_part2.sort(key=cmp_to_key(compare))
index1 = all_pairs_part2.index(divider1) + 1
index2 = all_pairs_part2.index(divider2) + 1
print(index1 * index2)
