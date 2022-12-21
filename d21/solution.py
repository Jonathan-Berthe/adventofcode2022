from sympy import symbols, solve

## Helper class
class Monkey:
  def __init__(self, name, input, all_monkeys):
    self.all_monkeys = all_monkeys
    self.name = name
    self.input = input
    self.num = None
    self.is_root = self.name == "root"
    self.is_human = self.name == "humn"
    if input.isdigit():
      self.num = int(input)
  
  def compute_operation_string(self):
    if self.is_human:
      return "x"
    if self.num is not None:
      return f"{self.num}"
    else:
      m1_name = self.input[0:4]
      m2_name = self.input[7:]
      operande = self.input[5]
      m1 = self.all_monkeys[m1_name]
      m2 = self.all_monkeys[m2_name]
      if self.is_root:
        operation = f"({m1.compute_operation_string()}) - ({m2.compute_operation_string()})"
      else:
        operation = f"({m1.compute_operation_string()}) {operande} ({m2.compute_operation_string()})"
      return operation

  def find_num(self):
    if self.num is not None:
      return self.num
    else:
      m1_name = self.input[0:4]
      m2_name = self.input[7:]
      m1 = self.all_monkeys[m1_name]
      m2 = self.all_monkeys[m2_name]
      operation = self.input
      locals()[m1_name] = m1.find_num()
      locals()[m2_name] = m2.find_num()
      return eval(operation)

## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""), f.readlines()))
all_monkeys = {}
for line in lines:
  tmp = line.split(": ")
  name = tmp[0]
  input = tmp[1]
  all_monkeys[name] = Monkey(name, input, all_monkeys)

print("SOLUTION PART 1:")
print(int(all_monkeys["root"].find_num()))

print("SOLUTION PART 2 ")
equation = all_monkeys["root"].compute_operation_string()
sol = solve(equation, symbols('x'))
print(int(sol[0]))
