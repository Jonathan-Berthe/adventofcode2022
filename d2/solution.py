with open('./input.txt') as f:
    lines = list(map(lambda line: line.replace("\n", ""),f.readlines()))

SCORES_SHAPE = {
  "X": 1,
  "Y": 2,
  "Z": 3
}
SCORES_OUTCOM = {
  "LOST": 0,
  "DRAW": 3,
  "WON": 6 
}

def result_of_round(round):
  a,b = round.split()
  if (a == "A" and b == "Y") or (a == "B" and b == "Z") or (a == "C" and b == "X"):
    return "WON"
  elif (a == "A" and b == "X") or (a == "B" and b == "Y") or (a == "C" and b == "Z"):
    return "DRAW"
  else:
    return "LOST"

def score_of_round(round):
  _a,b = round.split()
  score_shape = SCORES_SHAPE[b]
  score_outcom = SCORES_OUTCOM[result_of_round(round)]
  return score_shape + score_outcom

def map_round_for_p2(round):
  a,b = round.split()
  shape_to_do = None
  if b == "Z":
    shape_to_do = "Y" if a == "A" else ("Z" if a == "B" else "X")
  elif b == "Y":
    shape_to_do = "X" if a == "A" else ("Y" if a == "B" else "Z")
  else:
    shape_to_do = "Z" if a == "A" else ("X" if a == "B" else "Y")
  return f"{a} {shape_to_do}"


print("SOLUTION PART 1:")
print(sum(list(map(lambda round: score_of_round(round),lines))))

print("SOLUTION PART 2:")
mapped_lines = map(lambda round: map_round_for_p2(round), lines)
print(sum(list(map(lambda round: score_of_round(round),mapped_lines))))