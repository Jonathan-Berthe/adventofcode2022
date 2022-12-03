import heapq

with open('./input.txt') as f:
    lines = f.readlines()

sum_cal_by_reindeer = []
reindeer_cal_current = 0
for line in lines:
  cal = line.replace("\n", "")
  if len(cal) == 0:
    sum_cal_by_reindeer.append(reindeer_cal_current)
    reindeer_cal_current = 0
  else:
    reindeer_cal_current += int(cal)

print("SOLUTION PART 1:")
print(max(sum_cal_by_reindeer))

print("SOLUTION PART 2:")
print(sum(heapq.nlargest(3, sum_cal_by_reindeer)))