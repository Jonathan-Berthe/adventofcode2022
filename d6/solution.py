with open('./input.txt') as f:
  line = f.readline()

part = 2 # Variable: part = i => part i of exercise
interval = 4 if part == 1 else 14
solution = None
for idx in range(0, len(line) - interval - 1):
  substr = line[idx:idx + interval] # 4
  if len(set(substr)) == len(substr):
    solution = idx + interval
    break

print('SOLUTION PART '+ str(part) + ":" )
print(solution)
