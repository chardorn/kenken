import numpy
import random


#check to see if there are any other of the same letter in that row
def checkRow(grid, y):
  global a

  for x1 in range(a):
    for x2 in range(a):
      if(x1 == x2):
        continue
      elif(grid[x1][y].num == grid[x2][y].num):
        return False
  return True

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



#check to see if there are any other of the same letter in that column
def checkColumn(grid, x):
  global a

  for y1 in range(a):
    for y2 in range(a):
      if(y1 == y2):
        continue
      elif(grid[x][y1].num == grid[x][y2].num):
        return False
  return True

def checkGrid(grid):
  for x in range(a):
    if(checkColumn(x) == False):
      return false
  for y in range(a):
    if(checkRow(y) == False):
      return false
  #for Sections in Sections Array
    #checkSections for validity
  return true


#Checks to see if Section violates it's own 
  #Array of length is the numBoxes in the Section
  #Total is what they must equal combined
  #Func is either +, -, *, or /
def checkSection(arr, total, func):
  arr = sorted(arr)
  result = arr[0]
  print(result)
  for i in range(len(arr) - 1):
      if(func == '+'):
          result += arr[i + 1]
      elif(func == '-'):
          result -= arr[i + 1]
      elif(func == '*'):
          result *= arr[i + 1]
      elif(func == '/'):
          result /= arr[i + 1]
      print(result)
  if(result == total):
      return True
  else:
      return False


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




class Section:
  def __init__(self, letter, numEls):
    self.letter = letter
    self.numEls = numEls
    arr = []
    

  def getLetter(self):
    return self.letter

  def incEls():
    self.numElse += 1

class Box:
  def __init__(self, letter, xPos, yPos):
    self.letter = letter
    self.xPos = xPos
    self.yPos = yPos
    self.num = 0
    possible = []

  def printBox(self):
    print("Box letter is " + self.letter + " at " + str(self.xPos)
          + ", " + str(self.yPos))

  def constrained(box):
    return box.possibleValues



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

def splitRule(rule):
  global factor
  global operator
  for i in range(len(rule)):
    if(rule[i].isdigit()):
      factor += int(rule[i])
    else:
      operator += rule[i] or operator ==" "

#Iterate through and assign Section rules based on letter ID
ruleDict = dict.fromkeys(set(sectionRules), "")

for key in sorted(ruleDict):
  print("{}:".format(key), end = '')
  ruleDict[key] = str(input())
  #Convert incoming string into two parts: number and operator
  factor = 0
  operator = ""
  splitRule(str(input))
  ruleDict[key] = Section(factor, operator)

print(ruleDict)

print(a)
print(inputs)
printGrid(randomInit(fullGrid))
print("Is row valid?")
print(checkRow(fullGrid, 0))
print("Is column valid?")
print(checkColumn(fullGrid, 0))

