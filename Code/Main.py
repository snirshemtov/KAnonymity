import DBParser
from Functions import *

numOfPeople = 1000  # for no limit, insert '-1'
k = 10
l = 3 # choose from (1,2,3,4,5)

data = DBParser.makeListOfDictionaries(numOfPeople)
algorithm2(data, k, l)
