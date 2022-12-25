## Parse input
with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""), f.readlines()))

def number_to_base(n, b):
  if n == 0:
      return [0]
  digits = []
  while n:
      digits.append(int(n % b))
      n //= b
  return digits[::-1]

def convert_snafu_to_dec(snafu):
  len_snafu = len(snafu)
  total = 0
  for i in range(len_snafu):
    tmp = snafu[i]
    multiplicator = pow(5, len_snafu - i - 1)
    if tmp.isdigit():
      total += multiplicator * int(tmp)
    elif tmp == "=":
      total -= 2 * multiplicator
    elif tmp == "-":
      total -= multiplicator
  return total

# xn * 5^n + ... + x1 * 5^1 + x0 * 5^0 = c with -2 <= xi <= 2
# <=> (xn + 2) * 5^n + ... + (x1 + 2) * 5^1 + (x0 + 2) * 5^0 = c + 2 * 5^n + ... + 2 * 5^1 + 2 * 5^0
# <=> yn * 5^n + ... + y1 * 5^1 + y0 * 5^0 = c + 2 * 5^n + ... + 2 * 5^1 + 2 * 5^0 with 0 <= yi <= 4
# => we can find all yi with number_to_base(c + 2 * 5^n + ..., 5)
# => we find all xi with xi = yi - 2
def convert_dec_to_snafu(dec):
  max_exp = 25
  new_dec = dec
  mapping = ["=", "-", "0", "1", "2"]
  for i in range(max_exp):
    new_dec += 2 * pow(5, i)
  new_dec_base5 = number_to_base(new_dec, 5)
  out = ""
  for i in new_dec_base5:
    char_to_add = f"{mapping[i]}"
    if len(out) == 0 and char_to_add == "0":
      continue
    out += char_to_add
  return out

sol = 0
for line in lines:
  sol += convert_snafu_to_dec(line)

print("SOLUTION:")
print(convert_dec_to_snafu(sol))
