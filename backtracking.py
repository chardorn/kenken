import numpy
import random

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

  #grid[xPos][yPos].getSection().printSection()
  #print("With num = " + str(num))

  
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
    #print("FUNCTION IS NONE")
    if(newNum == total):
      return True
    else:
      return False
  
  #print(result)
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
  #print("1Result: " + str(result))




  #check to see if array is full (minus the last digit)
  #print(str(section.boxes[len(section.boxes) - 2].num))
  if(section.boxes[len(section.boxes) - 2].num != 0):
    #print("LAST BOX")
    if(func == '+'):
      result += newNum

      if(result == total): #Should eventually be changed to be == total
        return True
      else:
        return False
    elif(func == '*'):
      result *= newNum
      if(result == total): #Should eventually be changed to be == total
        return True
      else:
        return False
    elif(func == '-'):
      #print("Result: " + str(result))
      #CHEAP OUT:
      if(result - newNum < 0):
        result = newNum - result
        #print("HERE" + str(result))
      else:
        result -= newNum
      #print("Actual Result: " + str(result))
      if(result == section.total): #Should eventually be changed to be == total
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
      #print("Result: " + str(result))
      #print("Total: " + str(total))
      result = result/newNum


      if(result == section.total): #Should eventually be changed to be == total
        #print("TRUE")
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
        #print("Result: " + str(result))
        return True
      #print("Result: " + str(result))
      if(result >= section.total):
        return True
      else:
        return False
    elif(func == '/'):
      #print("HERE I AM")
      #print("Total: " + str(section.total))
      #result /= newNum
      if(result == 0):
        result += newNum
        #print("Result: " + str(result))
      if(result%newNum != 0):
        return False
      #if(result >= section.total):
        #return True
      #DEBUG
      return True

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
    #newBox.printBox()
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
      if(grid[x][y].num == 0):
        l[0] = x
        l[1] = y
        return True
  else:
    return False


def isSafe(grid, x, y, num):
    return(isRowSafe(grid, x, y, num) and isColumnSafe(grid, x, y, num) and isSectionSafe(grid, x, y, num))

#Recursive backtracking algorithm
#Current problem: sections are not resetting when backtracking
def solveSudoku(grid):
  global fullGrid
  global a
  global counter

  # 'l' is a list variable that keeps the record of row and col in find_empty_location Function     
  l=[0,0]
  
  if(nextNode(grid, l) == False):
    #print(str(l[0]) + " " + str(l[1]))
    fullGrid = grid
    return True

  xPos = l[0]
  yPos = l[1]


  #print("CurrentX: " + str(xPos) + " Current Y: " + str(yPos))

  #printGrid(grid)

  for num in range(1,a + 1):

    #print("Num: " + str(num))

    if (isSafe(grid, xPos, yPos, num)):
        counter += 1
        grid[xPos][yPos].num = num
        #print("It's safe")
        if(solveSudoku(grid)):
          
          return True
        else:
          grid[xPos][yPos].num = 0
          
          #printGrid(grid)



  #printGrid(grid)
  #print(False)
  return False

counter = 0
print(a)
printGrid(zeroInit(fullGrid))
print(solveSudoku(fullGrid))
print("COUNTER: "+ str(counter))
printGrid(fullGrid)
