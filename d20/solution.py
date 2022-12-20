import math

## Helper classes
class Digit:
  def __init__(self, value, pos):
    self.value = value
    self.position = pos

class Sequence:
  def __init__(self, initial_list):
    self.seq_list = initial_list
    self.len_seq = len(initial_list)
    self.iter_list = initial_list.copy()
    for digit in initial_list:
      if digit.value == 0:
        self.ref_digit = digit

  def move_digit(self, digit):
    previous_pos = digit.position
    new_pos = (previous_pos + digit.value) % (self.len_seq - 1) if digit.value > 0 else (self.len_seq - 1) - ((self.len_seq - 1 - previous_pos + abs(digit.value)) % (self.len_seq - 1))
    digit.position = new_pos
    if new_pos > previous_pos:
      for i in range(previous_pos, new_pos):
        digit_to_move = self.iter_list[i + 1]
        digit_to_move.position = i
        self.iter_list[i] = digit_to_move
    else:
      for i in range(previous_pos, new_pos, -1):
        digit_to_move = self.iter_list[i - 1]
        digit_to_move.position = i
        self.iter_list[i] = digit_to_move
    self.iter_list[new_pos] = digit

  def run_mixing(self):
    for digit in self.seq_list:
      self.move_digit(digit)
  
  def value_after_0(self, n):
    ref = self.ref_digit
    pos = (ref.position + n) % (self.len_seq)
    #print(pos)
    return self.iter_list[pos].value
  
  def grove_coordinates(self):
    sum = 0
    for i in [1000, 2000, 3000]:
      sum += self.value_after_0(i)
    return sum

## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: int(line.replace("\n", "")),f.readlines()))

print("SOLUTION PART 1:")
data_initial = [Digit(line, idx) for (idx, line) in enumerate(lines)]
s = Sequence(data_initial)
s.run_mixing()
result = s.grove_coordinates()
print(result)

print("SOLUTION PART 2:")
data_initial = [Digit(line * 811589153, idx) for (idx, line) in enumerate(lines)]
s = Sequence(data_initial)
for i in range(10):
  s.run_mixing()
result = s.grove_coordinates()
print(result)
