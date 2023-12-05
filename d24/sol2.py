from collections import defaultdict
import heapq

def read_input():
    dirdict = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}
    with open(r"input.txt") as f:
        lines = f.read().splitlines()
        board_height = len(lines) - 2
        board_width = len(lines[1]) - 2
        elf_start = (lines[0].index(".") - 1, -1)
        elf_end = (lines[-1].index(".") - 1, board_height)
        blizzards = [((x-1, y-1), dirdict[lines[y][x]]) \
            for y in range(1, board_height+1) for x in range(1, board_width+1) if lines[y][x] in dirdict]
        return elf_start, elf_end, blizzards, board_width, board_height

def move_blizzards(blizzards, time):
    if time in blizzard_dict: return blizzard_dict[time]
    stuff = defaultdict(list)
    for blizzard in blizzards:
        x, y = (blizzard[0][0] + blizzard[1][0] * time) % board_width, \
            (blizzard[0][1] + blizzard[1][1] * time) % board_height
        stuff[(x, y)].append(blizzard)
    blizzard_dict[time] = stuff
    return stuff

def calc_moves(pos, blizzards, time):
    delta_force = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    stuff = move_blizzards(blizzards, time+1)
    moves = []
    for delta in delta_force:
        x, y = pos[0] + delta[0], pos[1] + delta[1]
        if (x, y) not in stuff and ((x, y) == elf_end or (x, y) == elf_start or  x >= 0 and x < board_width and y >= 0 and y < board_height):
            moves.append((x, y))
    
    return moves

def find_path_time(blizzards, start_pos, end_pos, time):
    heap = []
    heapq.heappush(heap, (0, start_pos, time))
    visited = set()

    while heap:
        _, pos, time = heapq.heappop(heap)
        if pos == end_pos: return time
        if (pos, time) not in visited:
            visited.add((pos, time))
            for move in calc_moves(pos, blizzards, time):
                heapq.heappush(heap, (abs(pos[0] - end_pos[0]) + abs(pos[1] - end_pos[1]) + time, move, time+1))

elf_start, elf_end, blizzards, board_width, board_height = read_input()
blizzard_dict = {}

part1_time = find_path_time(blizzards, elf_start, elf_end, 0)
print ("Part 1:", part1_time)
part2_time = find_path_time(blizzards, elf_end, elf_start, part1_time)
print(part2_time - part1_time)
part3_time = find_path_time(blizzards, elf_start, elf_end, part2_time)
print(part3_time - part2_time)
#print ("Part 2:", find_path_time(blizzards, elf_start, elf_end, 
#        find_path_time(blizzards, elf_end, elf_start, part1_time)))

# 322 - 314 - 338