with open('./input.txt') as f:
  lines = list(map(lambda line: line.replace("\n", ""),f.readlines()))

class File:
  def __init__(self, size, name, parent):
    self.size = size
    self.name = name
    self.parent = parent

class Dir:
  def __init__(self, name, parent):
    self.name = name
    self.children = [] # Files or Dir
    self.parent = parent
  
  def add_child_file(self, size, name):
    self.children.append(File(size, name, self))
  
  def add_child_dir(self, name):
    candidate = self.child_dir_with_name(name)
    if candidate is not None:
      return candidate
    new_dir = Dir(name, self)
    self.children.append(new_dir)
    return new_dir
  
  def child_dir_with_name(self, name):
    filtered_list = list(filter(lambda child: child.__class__.__name__  == "Dir" and child.name == name, self.children))
    return None if len(filtered_list) == 0 else filtered_list[0]
  
  def chidren_dir(self):
    return list(filter(lambda child: child.__class__.__name__  == "Dir", self.children))

  def compute_size(self):
    size = 0
    for child in self.children:
      if child.__class__.__name__ == "File":
        size += child.size
      else:
        size += child.compute_size()
    return size

class Filesystem:
  def __init__(self, commands):
    self.outermost = Dir("/", None)
    self.current_dir = self.outermost
    self.compute_filesystem(commands)
    self.solution_p1 = 0
    self.candidate_solutions_p2 = []
  
  def compute_filesystem(self, commands):
    for command in commands:
      if command[0] == "$" and command[2:4] == "cd":
        name = command[5:]
        self.cd(name)
      elif command[0] == "$" and command[2:4] == "ls":
        continue
      elif command[0:3] == "dir":
        _, name = command.split()
        self.current_dir.add_child_dir(name)
      else:
        size, name = command.split()
        self.current_dir.add_child_file(int(size), name)

  def cd(self, name):
    if name == "/":
      self.current_dir = self.outermost
      return
    if name == "..":
      parent_dir = self.current_dir.parent
      self.current_dir = parent_dir
      return
    child_dir = self.current_dir.add_child_dir(name)
    self.current_dir = child_dir
  
  def add_file(self, size, name):
    self.current_dir.add_child_file(size, name)
  
  def add_dir(self, name):
    self.current_dir.add_child_dir(name)
  
  def compute_recursively_p1(self, dir):
    size_dir = dir.compute_size()
    if size_dir <= 100000:
      self.solution_p1 += size_dir
    children = dir.chidren_dir()
    for child in children:
      self.compute_recursively_p1(child)
  
  def solution_part1(self):
    self.compute_recursively_p1(self.outermost)
    return self.solution_p1
  
  def compute_recursively_p2(self, dir, space_to_delete):
    size_dir = dir.compute_size()
    if size_dir >= space_to_delete:
      self.candidate_solutions_p2.append(size_dir)
    children = dir.chidren_dir()
    for child in children:
      self.compute_recursively_p2(child, space_to_delete)
  
  def solution_part2(self):
    space_to_delete = 30000000 - (70000000 - self.outermost.compute_size())
    self.compute_recursively_p2(self.outermost, space_to_delete)
    return min(self.candidate_solutions_p2)

filesystem = Filesystem(lines)

print("SOLUTION PART 1:")
print(filesystem.solution_part1())

print("SOLUTION PART 2:")
print(filesystem.solution_part2())
