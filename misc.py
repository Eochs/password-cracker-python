#PA 4
# Spencer Ochs

import re
from collections import Counter #Counter used in word_count() function 

"Miscellaneous functions to practice Python"

class Failure(Exception):
    """Failure exception"""
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

# Problem 1

# data type functions

def closest_to(l,v):
    """Return the element of the list l closest in value to v.  In the case of
       a tie, the first such element is returned.  If l is empty, None is returned."""
    if v in l: return v
    else:
    #create tuple to store (distance to v, element with closest distance to v)
        closest = (abs(v - l[0]), l[0]) #initialize with first elem in list
        for x in l:
            if abs(x - v) < closest[0]: closest = (abs(x-v), x)
    return closest[1]

def make_dict(keys,values):
    """Return a dictionary pairing corresponding keys to values."""
    d = {}
    for i in range( len(keys) ):
        d[ keys[i] ] = values[i] #create new "key:value" entries in dictionary
    return d
    # return dict( izip(keys,values) )
   
# file IO functions
def word_count(fn):
    """Open the file fn and return a dictionary mapping words to the number
       of times they occur in the file.  A word is defined as a sequence of
       alphanumeric characters and _.  All spaces and punctuation are ignored.
       Words are returned in lower case"""
    f = open(fn, 'r') # read in txt file want to 
    lowerCaseText = f.read().lower() # puts file in all lower case
    file.close
    # use regular expressions to replace all symbols that are not lower case letters, numbers, spaces, apostrophe or underscore with a space 
    justWordsText = re.sub('[^a-z0-9\ \_]+', " ", lowerCaseText)
    wordsFromFile = list(justWordsText.split())
    
    # if want to make count for all words in "words" doc 
    #for w in words:
    #    wordDict[w] = wordsFromFile.count(w)
  
    wordDict = dict( Counter(wordsFromFile) ) # Counter counts number of occurences of each item in the list, dict converts to dictionary
    return wordDict










