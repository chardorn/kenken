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


#CURRENTLY this function will just check if there is any other of the same number in it
#does not take into account the type or total
def isSectionSafe(grid, xPos, yPos, num):
  global a
  #check to see if adding the variable will allow it to be safe still
  for i in range grid[xPos][yPos].numEls():
    if(getSection(grid[xPos][yPos]).arr[i] == num):
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

def zeroInit(fullGrid):
  global a
  for y in range(a):
    for x in range(a):
      fullGrid[x][y].num = 0
  return fullGrid




class Section:
  def __init__(self, letter, numEls, arr, ):
    self.letter = letter
    self.numEls = numEls
    self.arr = arr
    

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

for x in range(a):
  for y in range(a):
    newBox = Box('A', x, y)
    newBox.num = 0
    fullGrid[x][y] = newBox
    

#
#
#BEGIN BACKTRACKING ALGORITHM
#
#


def checkColumn(grid, xPos, yPos, num):
  global a

  for y in range(a):
    if(y == yPos):
      continue
    elif(fullGrid[xPos][y].num == num):
      return False
  return True


#currentX = 0
#currentY = 0

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

  


#NOTE: this only checks rows and columns right now
def isSafe(grid, x, y, num):
    return(isRowSafe(grid, x, y, num) and isColumnSafe(grid, x, y, num) and isSectionSafe())


#REMEMBER this is a grid of boxes! Not just integers
def solveSudoku(grid):
  global fullGrid
  global a

  # 'l' is a list variable that keeps the record of row and col in find_empty_location Function     
  l=[0,0]
  
  if(nextNode(grid, l) == False):
    print(str(l[0]) + " " + str(l[1]))
    fullGrid = grid
    return True

  xPos = l[0]
  yPos = l[1]

  print("CurrentX: " + str(xPos) + " Current Y: " + str(yPos))


  #Num range is ints from 1 to a
  for num in range(1,a + 1):

    #printGrid(grid) #FOR TESTING
    #printGrid(fullGrid)
    print(num)

    if (isSafe(grid, xPos, yPos, num)):
        grid[xPos][yPos].setNum(num)

        print(grid[xPos][yPos].num)

        if(solveSudoku(grid)):
          return True

        print(grid[xPos][yPos].num)

        grid[xPos][yPos].setNum = 0        

  print(False)
  return False

print(a)
printGrid(zeroInit(fullGrid))
print(solveSudoku(fullGrid))
printGrid(fullGrid)

    
  
