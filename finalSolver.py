import numpy
import random
from copy import copy, deepcopy
import queue


#
#CLASSES:
#

class Section:
  def __init__(self, letter, total, operator):
    self.total = total
    self.operator = operator
    self.letter = letter
    self.boxes = []
    self.possibleVals = []

  def printSection(self):
    print("Section " + self.letter)
    for i in range(len(self.boxes)):
      print("(" + str(self.boxes[i].xPos) +  ", " + str(self.boxes[i].yPos) + ") --> " + str(self.boxes[i].num))
    print("Total: " + str(self.total))

  def alreadyNum(self, num):
    for i in range(len(self.boxes)):
      if(self.boxes[i].num == num):
        return False
    return True
  
  def sortBoxes(self):
    self.boxes = sorted(self.boxes, key=lambda x: x.num, reverse=True)

  def updateSection(self):
    self.possibleVals = getPossibleVals(self)




class Box:
  
  def __init__(self, letter, xPos, yPos):
    global ruleDict
    self.letter = letter
    self.xPos = xPos
    self.yPos = yPos
    self.num = 0

  def printBox(self):
    print("Box letter is " + self.letter + " at " + str(self.xPos)
          + ", " + str(self.yPos))

  def getSection(self):
    return ruleDict[self.letter]

  def removePossible(self, num):
    
    if num in self.possibleVals:

      self.possibleVals.remove(num)

      return True
    else:
      return False

  def addPossible(self, num):

    self.possibleVals.append(num)

  def initPossibleVals(self):
    self.possibleVals = getPossibleVals(self.getSection())



#Relationship: 1 for column, 2  for row, 3 for Section
class Axiom:
  def __init__(self, box1, box2, num):
    self.box1 = box1
    self.box2 = box2
    self.num = num

  def runAxiom(self):
    return self.box2.removePossible(self.num)

  def reverseAxiom(self):
    self.box2.addPossible(self.num)

  def printAxiom(self):
    print("Axiom: [" + str(self.box1.xPos) + "][" + str(self.box1.yPos) + "] --> ["
          + str(self.box2.xPos) + "][" + str(self.box2.yPos) + "] " + str(self.num))


#
#INPUT helper functions
#


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



def getPossibleVals(section):
  factors = []
  if(section.operator == '*'):
    return getFactors(len(section.boxes), section.total)
  if(section.operator == '-' or section.operator == '/'):
    for i in range(a):
      factors.append(i+1)
    return factors
  for i in range(a):
    if((i+1) <= section.total):
      factors.append(i+1)
  return factors

#if string == '*'
def getFactors(numBoxes, total):
  global a
  factors = []

  for i in range(a):
    if((i+1) != 0 and total % (i+1) == 0):
        factors.append(i+1)
  return factors




#
#GATHERING INPUT
#
a = int(input())
fullGrid = [[0 for x in range(a)] for y in range(a)]
fullGrid2 = [[0 for x in range(a)] for y in range(a)]

sections = [0 for x in range(a)]
sections = [0 for x in range(a)]



inputs = []
boxes = []
simpleCount = 0
advancedCount = 0
localCount = 0
axiomQueue = queue.Queue()
undoQueue = queue.Queue()



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
  rule = str(input())
  ruleDict[key] = rule[2::]
  
  #Convert incoming string into two parts: number and operator
  factor = 0
  operator = ""
  splitRule(rule[2::])

  ruleDict[key] = Section(key, factor, operator)


#Go through and add letters to Sections
for i in range(a):
  for j in range(a):
    fullGrid[i][j].getSection().boxes.append(fullGrid[i][j])

for key in sorted(ruleDict):
  ruleDict[key].updateSection()
  ruleDict[key].printSection()

ruleDict2 = deepcopy(ruleDict)

#update Sections
for i in range(a):
  for j in range(a):
    fullGrid[i][j].initPossibleVals()

sections2 = deepcopy([0 for x in range(a)]


#
# FUNCTIONS
#

def isColumnSafe(grid, xPos, yPos, num):
  global a
  for y in range(a):
    if(y == yPos):
      continue
    elif(grid[xPos][y].num == num):
      return False
  return True

def isRowSafe(grid, xPos, yPos, num):
  global a
  for x in range(a):
    if(x == xPos):
      continue
    elif(grid[x][yPos].num == num):
      return False
  return True

def isSectionSafe(grid, xPos, yPos, num):
  print("Is Safe? " + str(xPos) + ", " + str(yPos) + "  " + str(num))
  global a
  
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

  if(func == ""):

    if(newNum == total):
      return True
    else:
      return False
  
  #total all of the values that  already exist in the array
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



  print("HERE ")
  section.printSection()
  print("Length1: " + str(len(section.boxes)))
  print("Value: " + str(section.boxes[len(section.boxes) - 2].num))



  #if array is full (minus the last digit)
  if(section.boxes[len(section.boxes) - 2].num != 0):
    print("LAST DIGIT")

    if(func == '+'):
      result += newNum

      if(result == total): 
        return True
      else:
        return False
    elif(func == '*'):
      result *= newNum
      if(result == total): 
        return True
      else:
        return False
    elif(func == '-'):
      if(result - newNum < 0):
        result = newNum - result
      else:
        result -= newNum
      if(result == section.total): 
        return True
      else:
        return False
    elif(func == '/'):
      if(result < newNum):
        if(newNum%result != 0):
          return False
        else:
          return True
      elif(result%newNum != 0):
        return False
      result = result/newNum

      if(result == section.total):
        return True
    

  else:
    if(func == '+'):
      result += newNum

      if(result <= total):
        return True
      else:
        return False
    elif(func == '*'):
      result *= newNum
      if(result <= total):
        return True
      else:
        return False
    elif(func == '-'):
      #CHEAP OUT:
      #if(result - newNum < 0):
        #result = newNum - result
  
      if(result == 0):
        result += newNum

        return True

      if(result >= section.total):
        return True
      else:
        return False
    elif(func == '/'):
      if(result == 0):
        result += newNum
      if(result%newNum != 0):
        return False

      return True

#print Grid
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







#finds the next node that is equal to 0
def nextNode(grid, l):
  global a
  for x in range(a):
    for y in range(a):
      if(grid[x][y].num == 0):
        l[0] = x
        l[1] = y
        return True
  else:
    return False


def isSafe(grid, x, y, num):
    printGrid(grid)
    return(isRowSafe(grid, x, y, num) and isColumnSafe(grid, x, y, num) and isSectionSafe(grid, x, y, num))

#SIMPLE backtracking algorithm
def solveSudoku(grid):
  global a
  global simpleCount
  simpleCount += 1


  # 'l' is a list variable that keeps the record of row and col in find_empty_location Function     
  l=[0,0]
  
  if(nextNode(grid, l) == False):
    printGrid(grid)
    return True

  xPos = l[0]
  yPos = l[1]

  for num in range(1,a + 1):


    if (isSafe(grid, xPos, yPos, num)):
        grid[xPos][yPos].num = num
        if(solveSudoku(grid)):
          return True
        else:
          grid[xPos][yPos].num = 0


#finds the next node that is equal to 0
def advancedNextNode(grid, l):
  global a
  l[0] = None
  l[1] = None
  max = a
  for x in range(a):
    for y in range(a):
      if(grid[x][y].num == 0 and len(grid[x][y].possibleVals) <= max):
        max = len(grid[x][y].possibleVals)
        l[0] = x
        l[1] = y

  if(l[0] == None):
    return False
  else:
    return True


#ADVANCED BACKTRACKING ALGORITHM
def solveWithArc(grid):
  #printGrid(grid)
  global advancedCount
  global a
  global axiomQueue

  advancedCount += 1

# 'l' is a list variable that keeps the record of row and col in find_empty_location Function     
  l=[0,0]
  
  if(advancedNextNode(grid, l) == False):

    printGrid(grid)
    return True

  xPos = l[0]
  yPos = l[1]

  theBox = grid[xPos][yPos]
  section = theBox.getSection()

  arr = sorted(theBox.possibleVals)

  for i in range(len(arr)):
      if(i >= len(arr)):
          continue

      num = arr[i]


      if (isSafe(grid, xPos, yPos, num)):

          grid[xPos][yPos].num = num


          #add axioms for columns
          for x in range(a):
            if(x != xPos):
                if num in grid[x][yPos].possibleVals:

                    axiomQueue.put(Axiom(theBox, grid[x][yPos], num))
          
          #add axioms for rows
          for y in range(a):
            if(y != yPos):
                if num in grid[y][xPos].possibleVals:
                    axiomQueue.put(Axiom(theBox, grid[xPos][y], num))
            
          #add axioms for section
          for i in range(len(section.boxes) - 1):
            if num in arr:
                axiomQueue.put(Axiom(theBox, section.boxes[i], num))
              
          while(axiomQueue.empty() !=  True):
              axiom = axiomQueue.get()
              if(axiom.runAxiom()):
                undoQueue.put(axiom)

          if(solveWithArc(grid)):
              return True
          else:
              while(undoQueue.empty() != True):
                undoAxiom = undoQueue.get()
                undoAxiom.reverseAxiom() 
              theBox.num =  0
              
  return False

print(a)

print("Grid initialized to all 0s:")

emptyGrid = zeroInit(fullGrid)
emptyGrid2  =  zeroInit(deepcopy(fullGrid))

printGrid(emptyGrid)

print("Simple grid:")
print(solveSudoku(emptyGrid))


print("Advanced grid:")
print(solveWithArc(deepcopy(emptyGrid2)))

print("SIMPLE COUNT: " + str(simpleCount))
print("ADVANCED COUNT: " + str(advancedCount))



