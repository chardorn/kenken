import random
import queue 

#
#HELPER FUNCTIONS
#

#Returns false if num already exists in column
def isColumnSafe(grid, xPos, yPos, num):
  global a
  for y in range(a):
    if(y == yPos):
      continue
    elif(grid[xPos][y].num == num):
      return False
  return True

#Returns false if num already exists in row
def isRowSafe(grid, xPos, yPos, num):
  global a
  for x in range(a):
    if(x == xPos):
      continue
    elif(grid[x][yPos].num == num):
      return False
  return True

#Returns false if num already exists in Section or if num violates section rules
def isSectionSafe(grid, xPos, yPos, num):
  global a

  #check to see if number is already in Section
  for i in range(grid[xPos][yPos].num):
    if(grid[xPos][yPos].getSection().alreadyNum(num) == False):
      return False

  #check to see if number is valid based on Section Rules
  if(checkSectionRules(grid[xPos][yPos].getSection(), num)):
    return True


  #Checks to see if Section violates its rules if newNum is added
  #Array of length is the numBoxes in the Section
  #Total is what they must equal combined
  #Func is either +, -, *, or /
def checkSectionRules(section, newNum):
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





  #if adding another number will make the array full, check that the total == result
  if(section.boxes[len(section.boxes) - 2].num != 0):

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
      result = result / newNum


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

#Parameters: section to find possible values of 
#Return array of factors based on total of section
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



#print grid function
def printGrid(fullGrid):
  global a
  for y in range(a):
    print("")
    for x in range(a):
      print(fullGrid[x][y].num, end = ' ')
  print("")

#Initialize given grid so all Box.num are set to 0
def zeroInit(fullGrid):
  global a
  for y in range(a):
    for x in range(a):
      fullGrid[x][y].num = 0
  return fullGrid


#Used to take input and turn into a factor and an operator
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

#
##CLASSES:
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

  #Returns true if num already exists in array possibleVals
  def alreadyNum(self, num):
    for i in range(len(self.boxes)):
      if(self.boxes[i].num == num):
        return False
    return True
  
  #Modifies self.boxes so the values are in ascending order
  def sortBoxes(self):
    self.boxes = sorted(self.boxes, key=lambda x: x.num, reverse=True)

  #Used to add possibleVals to all the number after the section input is given
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

  #Returns false if num is not in array possibleVals
  #Returns true if num is sucessfully removed from possibleVals
  def removePossible(self, num):
    if num in self.possibleVals:
      self.possibleVals.remove(num)
      return True
    else:
      return False

  #Adds num to possibleVals
  def addPossible(self, num):
    self.possibleVals.append(num)

  #Used to add possibleVals to all the number after the section input is given
  def initPossibleVals(self):
    self.possibleVals = getPossibleVals(self.getSection())


#Parameters: box1 one is modified and possibleVals of box2 must be changed in response
            #num is the value that was changed from box1
class Axiom:
  def __init__(self, box1, box2, num):
    self.box1 = box1
    self.box2 = box2
    self.num = num

  #Return true if num is present in possibleVals and is sucesfully removed, false otherwise
  def runAxiom(self, grid):
    if(advancedCheckSection(grid, self.box1, self.box2)):
      return self.box2.removePossible(self.num)
    else:
      return False

  #Add num back to possibleVals
  def reverseAxiom(self):
    self.box2.addPossible(self.num)

  def printAxiom(self):
    print("Axiom: [" + str(self.box1.xPos) + "][" + str(self.box1.yPos) + "] --> ["
          + str(self.box2.xPos) + "][" + str(self.box2.yPos) + "] " + str(self.num))
    

#
# GET INPUT
#


a = int(input())
fullGrid = [[0 for x in range(a)] for y in range(a)]
sections = [0 for x in range(a)]

inputs = []
boxes = []
counter = 0



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

#update Sections
for i in range(a):
  for j in range(a):
    fullGrid[i][j].initPossibleVals()

#
#MORE HELPER FUNCTIONS:
#

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

#checks box2 to of an axiom to see if it causes any other values to become invalid
#Removes any possibleVals that have become invalid due to axiom that was run
def advancedCheckSection(grid, box1, box2):
  atLeastOneValue = False
  section = box2.getSection()
  arr = box2.possibleVals
  
  #Iterate through possibleVals and check if isSafe()
  for i in range(len(arr) - 1):
    if(i >= len(arr) - 1):
      continue
    arr = box2.possibleVals
    if(isSafe(grid, box2.xPos, box2.yPos, arr[i])):
      atLeastOneValue = True
    else:
      
      undoQueue.put(Axiom(box1, box2, arr[i]))
      box2.possibleVals.remove(arr[i])

#Checks row, column, and section with new num
def isSafe(grid, x, y, num):
    return(isRowSafe(grid, x, y, num) and isColumnSafe(grid, x, y, num) and isSectionSafe(grid, x, y, num))


def solveWithArc(grid):
  global fullGrid
  global a
  global count
  global axiomQueue
  #printGrid(grid)
  count += 1

# 'l' is a list variable that keeps the record of row and col in find_empty_location Function     
  l=[0,0]
  
  if(advancedNextNode(grid, l) == False):

    fullGrid = grid
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

      #Check column, row, and section to see if number is valid
      if (isSafe(grid, xPos, yPos, num)):
          grid[xPos][yPos].num = num

          #add axioms for columns to queue
          for x in range(a):
            if(x != xPos):
                if num in grid[x][yPos].possibleVals:

                    axiomQueue.put(Axiom(theBox, grid[x][yPos], num))
          
          #add axioms for rows to queue
          for y in range(a):
            if(y != yPos):
                if num in grid[y][xPos].possibleVals:
                    axiomQueue.put(Axiom(theBox, grid[xPos][y], num))
            
          #add axioms for section to queue
          for i in range(len(section.boxes) - 1):
            if num in arr:
                axiomQueue.put(Axiom(theBox, section.boxes[i], num))
              
          #Iterate through all axioms in queue 
          #If runAxiom returns true (meaning the num did exist and was removed from possibleVals) add the axiom to undoQueue
          while(axiomQueue.empty() !=  True):
              axiom = axiomQueue.get()
              if(axiom.runAxiom(grid)):
                undoQueue.put(axiom)

          #Recursively call solveWithArc to go to next node
          if(solveWithArc(grid)):
              return True
          else:
              #If solveWithArc returns false, undo the arc consistency that was previously carried out
              #Iterate through undoqueue and add back values to possibleVals
              while(undoQueue.empty() != True):
                undoAxiom = undoQueue.get()
                undoAxiom.reverseAxiom() 
              theBox.num =  0
              
  return False

  #
  #MAIN CODE:
  #


axiomQueue = queue.Queue()
undoQueue = queue.Queue()

count = 0

print("Grid initialized to all 0s:")
printGrid(zeroInit(fullGrid))

print(solveWithArc(fullGrid))
printGrid(fullGrid)
print("FINAL COUNT: " + str(count))