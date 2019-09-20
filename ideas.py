a = 10

#if string == '*'  
def getFactorCombos(numBoxes, total):
  global a
  factors = []
  product = 1

  for i in range(a):
    print("i: " + str(i))
    if(i != 0):
       if(total % i == 0):
          print("True")  
          factors.append(i)
  #for x in range(len(factors)):
    #for y in range(numBoxes):
      #product *= factors[y]
    #if(product == total):
      #return factors
  return factors

print(str(getFactorCombos(3,12)))

