## Helpers methods and PairSB class
def manathan(x1, x2):
  return abs(x1[0] - x2[0]) +  abs(x1[1] - x2[1])

# copy paste from https://stackoverflow.com/questions/15273693/union-of-multiple-ranges
def union(segments):
  b = []
  for begin,end in sorted(segments):
    if b and b[-1][1] >= begin - 1:
      b[-1][1] = max(b[-1][1], end)
    else:
      b.append([begin, end])
  return b

def intersection(interval1, interval2):
  return [max(interval1[0], interval2[0]), min(interval1[1], interval2[1])]

class PairSB:
  def __init__(self, sensor, closest_beacon):
    self.sensor = sensor
    self.closest_beacon = closest_beacon
    self.distance = manathan(sensor, closest_beacon)

## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""),f.readlines()))

data = []
x_intervals_to_check = []
for line in lines:
  tmp = line.split(":")
  y_sensor = int(tmp[0].split(", y=")[1])
  x_sensor = int(tmp[0].split(", y=")[0].split("Sensor at x=")[1])
  y_beacon = int(tmp[1].split(", y=")[1])
  x_beacon = int(tmp[1].split(", y=")[0].split("closest beacon is at x=")[1])
  pair = PairSB([x_sensor, y_sensor], [x_beacon, y_beacon])
  data.append(pair)

## Solution
part = 2 # Variable: part = i => part i of exercise
max_pos = 4000000
range_y = [2000000] if part == 1 else range(0, max_pos + 1)
for y_to_test in range_y:
  count = 0
  segments = []
  for pair in data:
    c = pair.sensor[1]
    h = abs(c - y_to_test)
    delta_x = pair.distance - h
    if delta_x < 0:
      continue
    segments.append(sorted([pair.sensor[0] - delta_x, pair.sensor[0] + delta_x]))

  if part == 1:
    cannot_contain_beacon_ranges = union(segments)
    print("SOLUTION PART 1:")
    print(cannot_contain_beacon_ranges[0][1] - cannot_contain_beacon_ranges[0][0])
  else:
    cannot_contain_beacon_ranges = list(map(lambda segment: intersection(segment, [0, max_pos]), union(segments)))
    if len(cannot_contain_beacon_ranges) > 1:
      print("SOLUTION PART 2:")
      tuning_freq = (cannot_contain_beacon_ranges[0][1] + 1) * 4000000 + y_to_test
      print(tuning_freq)
      break
