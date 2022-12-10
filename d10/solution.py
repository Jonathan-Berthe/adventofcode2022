with open('./input.txt') as f:
    lines = list(map(lambda line: line.split(), list(map(lambda line: line.replace("\n", ""),f.readlines()))))

class Program:
    def __init__(self, instructions):
        self.instructions = instructions
        self.current_cycle = 0
        self.x_value = [1] # x_value[i] => value of x at start of cycle i + 1
        self.pixels = ""
        self.run_instructions()
    
    def noop(self):
        self.draw_pixel()
        self.current_cycle += 1
        self.x_value.append(self.x_value[self.current_cycle - 1])
    
    def addx(self, v):
        value_x_before_cycle = self.x_value[self.current_cycle]
        self.draw_pixel()
        self.current_cycle += 1
        self.draw_pixel()
        self.current_cycle += 1
        self.x_value.extend([value_x_before_cycle, value_x_before_cycle + v])
    
    def draw_pixel(self):
        horizontal_x_before_cycle = self.x_value[-1] % 40
        horizontal_pos_pixel_to_add = len(self.pixels) % 40
        if (horizontal_pos_pixel_to_add >= horizontal_x_before_cycle - 1 and horizontal_pos_pixel_to_add <= horizontal_x_before_cycle + 1):
            self.pixels += "#"
        else:
            self.pixels += "."

    def run_instructions(self):
        for instruction in self.instructions:
            if instruction[0] == "noop":
                self.noop()
            else:
                self.addx(int(instruction[1]))
    
    def strength(self, cycle):
        if (cycle > len(self.x_value) - 1):
            return None
        return cycle * self.x_value[cycle - 1]

    def solution_p1(self):
        out = 0
        for cycle in [20, 60, 100, 140, 180, 220]:
            out += self.strength(cycle)
        return out

p = Program(lines)
print("SOLUTION PART 1:")
print(p.solution_p1())

print("SOLUTION PART 2:") # put your terminal in 40 pixel width and look at the letters ^^
print(p.pixels)
