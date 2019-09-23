import numpy
import random
from random import shuffle
from functools import reduce

global constraintCount

constraintCount = 0

#check to see if there are any other of the same letter in that row
def checkRow(box):
  global fullGrid
  global a
  global constraintCount

  for x in range(a):
    if(x == box.xPos):
      continue
    elif(fullGrid[x][box.yPos].num == box.num):
      constraintCount += 1
      # return False
  # return True

#print grid
def printGrid(fullGrid):
  global a
  for y in range(a):
    print("")
    for x in range(a):
      print(fullGrid[x][y].num, end = ' ')
  print("")

def randomInit(fullGrid):
  global a
  numberList = list(range(1, a + 1))
  for y in range(a):
    shuffle(numberList)
    for x in range(a):
      for value in numberList:
          fullGrid[x][y].num = value
  return fullGrid

def splitRule(rule):
  global factor, operator
  factorStr = ""
  for i in range(len(rule)):
    if(rule[i].isdigit()):
      factorStr += rule[i]
    else:
      #Check for if rule exists or not
      operator += rule[i] or operator == None
  #Convert factor from str to int
  factor = int(factorStr)

##CLASSES:

class Section:
  def __init__(self, letter, total, operator):
    self.total = total
    self.operator = operator
    self.letter = letter
    self.boxes = []


  def printSection(self):
    print("Section " + self.letter)
    for i in range(len(self.boxes)):
      print("(" + str(self.boxes[i].xPos) +  ", " + str(self.boxes[i].yPos) + ") --> " + str(self.boxes[i].num))

  def alreadyNum(self, num):
    for i in range(len(self.boxes)):
      if(self.boxes[i].num == num):
        return False
    return True
  
  def sortBoxes(self):
    self.boxes = sorted(self.boxes, key=lambda x: x.num, reverse=True)




class Box:
  
  def __init__(self, letter, xPos, yPos):
    
    self.letter = letter
    self.xPos = xPos
    self.yPos = yPos
    self.num = 0    

  def printBox(self):
    print("Box letter is " + self.letter + " at " + str(self.xPos)
          + ", " + str(self.yPos))

  def getSection(self):
    return ruleDict[self.letter]

    
a = int(input())
fullGrid = [[0 for x in range(a)] for y in range(a)]
sections = [0 for x in range(a)]

inputs = []
boxes = []



#We'll now begin the Fitness-gram Pacer Test (SectionRules)
sectionRules = []
#Iterate down rows to add Strings of characters to array
y = 0
while(y < a):
  b = str(input())

  # Find all unique section letters (set)
  sectionRules.extend(list(b))

  inputs.append(b)

  #Iterate through characters in each array and make new Boxes
  x = 0
  while(x < a):
    newBox = Box(b[x], x, y)
    newBox.printBox()
    fullGrid[x][y] = newBox
    x += 1
  y += 1


#Iterate through and assign Section rules based on letter ID
ruleDict = dict.fromkeys(set(sectionRules), "")

for key in sorted(ruleDict):
  #print("{}:".format(key), end = '')
  rule = str(input())
  ruleDict[key] = rule[2::]
  
  #Convert incoming string into two parts: number and operator
  factor = 0
  operator = ""
  splitRule(rule[2::])
  #print(factor) #FOR TESTING
  #print(operator) #FOR TESTING
  ruleDict[key] = Section(key, factor, operator)

#Go through and add letters to Sections
for i in range(a):
  for j in range(a):
    fullGrid[i][j].getSection().boxes.append(fullGrid[i][j])
  
for key in sorted(ruleDict):
  ruleDict[key].printSection()














#MORE HELPER FUNCTIONS:

#check to see if there are any other of the same letter in that column
#this should ultimately increase our constraintCount by the amount of duplicates found in each column of the grid
def checkGrid(grid):
  global fullGrid
  global a
  global constraintCount

  for x in range(a):
    tempArr = []
    for y in range(a):
      if grid[x][y].num in tempArr:
        constraintCount += 1
      tempArr.append(grid[x][y].num)

  for y in range(a):
    tempArr = []
    for x in range(a):
      if grid[x][y].num in tempArr:
        constraintCount += 1
      tempArr.append(grid[x][y].num)

#To swap the numbers in boxes and ultimately reevaluate our utility function
#This should be able to swap two numbers in a given row, although not quite sure how this would work b/c we really do not
#Have a 2-D array/matrix of numbers, but instead a bunch of sections and boxes (Not sure how to iterate through these effectively)

def swap(grid, box1, box2):
  tmp = box1.num
  box1.num = box2.num
  box2.num = tmp

#This should calculate the current result of the randomized inputs for each section, and compare it to the actual result
#That difference should also increment the constraintCount variable, which acts as our utility function
def sectionDifference(section):
  global constraintCount
  func = section.operator
  goal = section.total
  arr = section.boxes
  result = 0

  if (func == '+'):
      result = reduce(lambda x, y: x + y.num, arr, 0)
  if (func == '-'):
      result = max(map(lambda i: i.num, arr)) - min(map(lambda i: i.num, arr))
  if (func == '/'):
      result = max(map(lambda i: i.num, arr)) - min(map(lambda i: i.num, arr))
  if (func == '*'):
      result = reduce(lambda x, y: x * y.num, arr, 0)
  if (func == ' '):
      result = goal

#   result = arr[0].num
#   for i in range(len(arr)-1):
#     if(arr[i + 1].num ==  0):
#       continue
#     if(func == '+'):
#         result += arr[i + 1].num
#     elif(func == '-'):
#         result = max(result, arr[i + 1].num) - min(result, arr[i + 1].num)
#     elif(func == '*'):
#         result *= arr[i + 1].num
#     elif(func == '/'):
#         result = max(result, arr[i + 1].num)/min(result, arr[i + 1].num)
#     elif(func == ' '):
#         result = total
#   # print(result)
#   # print(total)
      
  constraintCount += int(abs(goal - result))

# Our cost value fn =  num dups in each row/column + difference in section expected and actual value
def constraintFinder(grid):
  global constraintCount
  global sectionVal

  constraintCount = 0

  checkGrid(grid)

  print(constraintCount)

  sectionVal = list(ruleDict.values())

  for section in sectionVal:
    sectionDifference(section)

  return constraintCount

#Pseudocode for Local Search (hill climbing with simulated annealing)
# From a random initial state:
# cost = cost of current state
# alpha = predetermined constant
# while cost > 0
#     Choose a random neighbor n of the current state
#     new_cost = cost of n
#     probability = exp^((cost – new_cost)/temperature)
#     if probability > 1 then
#         current state = n
#         cost = new_cost
#     else
#         random(0,1)
#         if random < probability then
#         current state = n
#         cost = new_cost
#     temperature *= alpha

# The 6x6 calcudoku is a similar constraint satisfaction problem as it 
# also has constraints for which an evaluation function can be applied. A 
# state for the calcudoku grid is an assignment of numbers 1 to 6 to each 
# of the 6 rows as seen in figure 4. The evaluation function calculates the 
# cost by calculating the number of duplicates in each column and adding it 
# to the cost. For each cage, the result of the numbers is calculated and 
# compared to the result the cage should have. The difference is then added 
# to the cost. For example, the first column in figure 4 has 2 duplicates, 
# this cost of 2 will be added to the total cost for that grid. The top left 
# cage in figure 4 shows a multiplication operator and a result of 24. The 
# result of the numbers entered within this cage is equal to 10, this is a 
# difference of 14. This also will be added to the total cost of the grid. 
# The neighboring search space of a state is the collection of switches 
# between two numbers within a row. Thus, the hill climbing algorithm 
# calculates the cost of each possible switch within the rows. If the cost 
# of the lowest scoring neighboring state is lower than the current state 
# cost, then the calcudoku grid is updated. Similar to the 8-queens’ problem, 
# the algorithm iteratively computes this step until the cost is zero or no 
# better moves are possible.

def solveLocal(grid, attempts = set([])):
  global fullGrid
  global a
  global constraintCount
  global sectionVal

  # First randomly initialize the grid this should be done outside solveLocal
  # randomInit(fullGrid)
  grid = fullGrid
  count = constraintFinder(grid)

  if count == 0:
    return grid
    printGrid(grid)
  
  # Our cost value fn =  num dups in each row/column + difference in section expected and actual value
  # checkGrid(grid)

  sectionVal = list(ruleDict.values())

  # for(section in sorted(sectionVal)):
  #   sectionDifference(section)

  # Our randomized change will be a random assignment to random box
  # We should theoretically be able to sort each section by number of constraints (i.e. number of boxes)
  for section in sectionVal:
    # print(section.letter)
    for box in section.boxes:
      #print(box.num)
      tmp = box.num
      box.num = random.randint(1, a)
      tries = 0
      while map(tuple,grid) in attempts:
        box.num = random.randint(1, a)
        tries += 1
        if tries > a:
            break
      if tries > a:
        continue
      printGrid(grid)
      print("Original constraintCount is:", constraintFinder(grid))
      #recalculate cost value fn, if the cost of the lowest scoring neighboring state is lower, update grid
      if constraintFinder(grid) == 0:
        printGrid(grid)
        return
      elif constraintFinder(grid) <= count:
        count = constraintFinder(grid)
        print(count)
        continue
      if count == 0:
        return
      else:
        attempts.add(map(tuple,grid))
        solveLocal(grid, attempts)
        continue

    # tempGrid = grid
    # if constraintFinder(grid) != 0:
    #   solveLocal(tempGrid)


  # #rinse and repeat
  # solveLocal(grid)


print(a)
printGrid(randomInit(fullGrid))
print(solveLocal(fullGrid))
printGrid(fullGrid)

#######################################################################################################