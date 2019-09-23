import numpy
import random

global constraintCount

constraintCount = -1

def randomInit(fullGrid, a):
  for y in range(a):
    for x in range(a):
      fullGrid[x][y].num = random.randint(1,a)
  return fullGrid

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

def isColumnSafe(grid, xPos, yPos, num):
  global a
  for y in range(a):
    if(y == yPos):
      continue
    elif(fullGrid[xPos][y].num == num):
      return False
  return True

def isRowSafe(grid, xPos, yPos, num):
  global a
  for x in range(a):
    if(x == xPos):
      continue
    elif(fullGrid[x][yPos].num == num):
      return False
  return True

def isSectionSafe(grid, xPos, yPos, num):
  global a
  #section = grid[xPos][yPos].getSection()

  grid[xPos][yPos].getSection().printSection()
  print("With num = " + str(num))

  
  #check to see if number is already in Section
  for i in range(grid[xPos][yPos].num):
    if(grid[xPos][yPos].getSection().alreadyNum(num) == False):
      return False

  #check to see if number is valid based on Section Rules
  if(isSection(grid[xPos][yPos].getSection(), num)):
    return True


#Checks to see if Section violates its rules
  #Array of length is the numBoxes in the Section
  #Total is what they must equal combined
  #Func is either +, -, *, or /
def isSection(section, newNum):
  
  section.sortBoxes();
  func = section.operator
  total = section.total
  arr = section.boxes
  result = arr[0].num
  print(result)
  for i in range(len(arr)-1):
      if(arr[i + 1].num ==  0):
        continue
      if(func == '+'):
          result += arr[i + 1].num
      elif(func == '-'):
          result -= arr[i + 1].num
      elif(func == '*'):
          result *= arr[i + 1].num
      elif(func == '/'):
          result /= arr[i + 1].num
  print("1Result: " + str(result))




  #check to see if array is full (minus the last digit)
  print(str(section.boxes[len(section.boxes) - 2].num))
  if(section.boxes[len(section.boxes) - 2].num != 0):
    print("LAST BOX")
    if(func == '+'):
      result += newNum

      if(result == total):
        return True
      else:
        constraintCount += 1
        return False
    elif(func == '*'):
      result *= newNum
      if(result == total):
        return True
      else:
        constraintCount += 1
        return False
    elif(func == '-'):
      print("Result: " + str(result))
      #CHEAP OUT:
      if(result - newNum < 0):
        result = newNum - result
        print("HERE" + str(result))
      else:
        result -= newNum
      print("Actual Result: " + str(result))
      if(result == section.total):
        return True
      else:
        constraintCount += 1
        return False
    elif(func == '/'):
      if(result < newNum):
        if(newNum%result != 0):
          constraintCount += 1
          return False
        else:
          return True
      elif(result%newNum != 0):
        constraintCount += 1
        return False
      print("Result: " + str(result))
      print("Total: " + str(total))

      if(result == section.total):
        print("TRUE")
        return True
    

  else:
    if(func == '+'):
      result += newNum

      if(result <= total):
        return True
      else:
        constraintCount += 1
        return False
    elif(func == '*'):
      result *= newNum
      if(result <= total):
        return True
      else:
        constraintCount += 1
        return False
    elif(func == '-'):
      #CHEAP OUT:
      #if(result - newNum < 0):
        #result = newNum - result
  
      if(result == 0):
        result += newNum
        print("Result: " + str(result))
        return True
      print("Result: " + str(result))
      if(result >= section.total):
        return True
      else:
        constraintCount += 1
        return False
    elif(func == '/'):
      print("HERE I AM")
      print("Total: " + str(section.total))
      #result /= newNum
      if(result == 0):
        result += newNum
        print("Result: " + str(result))
      if(result%newNum != 0):
        constraintCount += 1
        return False
      #if(result >= section.total):
        #return True
      #DEBUG
      return True

#if string == '*'  
def getFactorCombos(numBoxes, total):
  global a
  factors = []

  for i in range(a):
    if(i != 0):
       if(total % i == 0):
          factors.append(i)
  for x in range(factors.length):
    for y in range(numBoxes):
      product *= factors[y]
    if(product == total):
      return factors

#if string == "/"
def getDivCombos(numBoxes, total):
  global divNum
  factors = []

  for i in range(divNum):
    if(i != 0):
      if(i % total == 0):
        factors.append(i)
  for x in range(factors.length):
    for y in range(numBoxes):
      div == max(div, factors[y]) / min(div, factors[y])
    if(div == total):
      return factors

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
  for y in range(a):
    for x in range(a):
      fullGrid[x][y].num = random.randint(1,a)
  return fullGrid

def zeroInit(fullGrid):
  global a
  for y in range(a):
    for x in range(a):
      fullGrid[x][y].num = 0
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

#finds the next node that is equal to 0
def nextNode(grid, l):
  global a
  for x in range(a):
    for y in range(a):
      # if(grid[x][y].num == 0):
      l[0] = x
      l[1] = y
      return True
  else:
    return False


def isSafe(grid, x, y, num):
    return(isRowSafe(grid, x, y, num) and isColumnSafe(grid, x, y, num) and isSectionSafe(grid, x, y, num))

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
  total = section.total
  arr = section.boxes
  result = arr[0].num
  for i in range(len(arr)-1):
    if(arr[i + 1].num ==  0):
      continue
    if(func == '+'):
        result += arr[i + 1].num
    elif(func == '-'):
        result = max(result, arr[i + 1].num) - min(result, arr[i + 1].num)
    elif(func == '*'):
        result *= arr[i + 1].num
    elif(func == '/'):
        result = max(result, arr[i + 1].num)/min(result, arr[i + 1].num)
    elif(func == ' '):
        result = total
    print(result)
    print(total)
      
  constraintCount += int(abs(total - int(result)))

# Our cost value fn =  num dups in each row/column + difference in section expected and actual value
def constraintFinder(grid):
  global constraintCount
  global sectionVal
  checkGrid(grid)

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

def solveLocal(grid):
  global fullGrid
  global a
  global constraintCount
  global sectionVal

  # First randomly initialize the grid this should be done outside solveLocal
  # randomInit(fullGrid)
  grid = fullGrid
  constraintCount = 0
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
      printGrid(grid)
      print(constraintFinder(grid))
      #recalculate cost value fn, if the cost of the lowest scoring neighboring state is lower, update grid
      if constraintFinder(grid) < 1:
        printGrid(grid)
        return grid
      elif constraintFinder(grid) < count:
        count = constraintFinder(grid)
        continue
      if count == 0:
        break
      else:
        box.num = tmp
        continue




  # #rinse and repeat
  # solveLocal(grid)


print(a)
printGrid(randomInit(fullGrid))
print(solveLocal(fullGrid))
printGrid(fullGrid)

#######################################################################################################

# #Local search algorithm
# #Current problem: literally nothing works
# def solveSudoku(grid):
#   global fullGrid
#   global a

#   # 'l' is a list variable that keeps the record of row and col in find_empty_location Function     
#   l=[0,0]
  
#   if(isSafe(grid, xPos, yPos, num)) == False):
#     print(str(l[0]) + " " + str(l[1]))
#     fullGrid = grid
#     return True

#   xPos = l[0]
#   yPos = l[1]

#   a = len(grid)
#   count = 0
#   max_swaps = a*a*(a-1) / 2

#   while(not solveSudoku):
#     randomInit(grid)
#     for x in range(0, max_swaps):
#       b1 = None
#       b2 = None
#       max_violations = 3*a*a

#       for i in range(0, a + 1):
#         for j in range(0, a):
#             for k in range(j + 1, a + 1 ):
#               swap(grid, grid[i][j], grid[i][k])

#               if not isSafe(grid, xPos, yPos, i) or constraintCount <= max_violations:
#                 b1 = grid[i][j]
#                 b2 = grid[i][k]
#                 max_violations = constraintCount
#                 solveSudoku(grid)
#               elif isSafe(grid, xPos, yPos, i):
#                 solveSudoku(grid)
#                 return True
              
#               swap(grid, grid[i][j], grid[j][k])
#       if b1 == None:
#         break
#       swap(grid, grid[i][j], grid[i][k])
#       count += 1
#   printGrid(grid)
#   return False