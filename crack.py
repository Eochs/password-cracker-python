# PA5
# Spencer Ochs 

from misc import *
import crypt

def load_words(filename,regexp):
    """Load the words from the file filename that match the regular
       expression regexp.  Returns a list of matching words in the order
       they are in the file."""
    f = open(filename, 'r')
    text = f.read()
    f.close()
    # findall() matches all occurrences of a regexp in text and returns as list
    #return re.findall(regexp, text)    
    reComp = re.compile(regexp)
    reMatchList = []
    # split text into list of words then populate the list with those words that match the passed in regexp
    for word in text.split('\n'):
        if reComp.match(word):
            reMatchList.append(word)
    return reMatchList
        

def transform_reverse(str):
    """Returns a list with with the original string and the reversal of that string"""
    return [str, "".join(reversed(str))]


def transform_capitalize(str):
    """Returns a list of all the possible ways to capitalize the input str"""
    strList = []
    
    # create recursive calls with helper function where each call is a branch
    # where either the ith char in the list is upper case or lower case
    def recHelper(prevStr, string, strList):
        # base case
        if len(string) == 1:
            strList.append( prevStr + string.upper() )
            strList.append( prevStr + string.lower() )
            return strList        
        # recursive case splits into two paths where one has first char of previous string capitalized, and the other where first char is lower case
        recHelper(prevStr + string[0].upper(), string[1:], strList)
        recHelper(prevStr + string[0].lower(), string[1:], strList)
                
    recHelper("", str, strList)
    return strList


def transform_digits(str):
    """Returns a list of all the possible ways to replace letters with similar looking digits according to the mapping of dMap. Last elem of list is original word str"""
    dMap = {
            "o": "0",
            "i": "1",
            "l": "1",
            "z": "2",
            "e": "3",
            "a": "4",
            "s": "5",
            "t": "7",
            "b": "6",
            "B": "8"
           }
    
    strList = [] # mutable value that is changed by recHelper
    # helper function to check if char should be switched to digit
    def toDigit(c):
        if c in dMap: return dMap[c]
        else: return c   
    # recursive helper function that, similar to the helper for
    # transform_capatalize(), recursively explores every path that either has
    # a letter replaced with its respective digit, or not.
    def recHelper(prevStr, string, strList):
        # base case
        if len(string) == 1:
            if string in dMap: # only take this path 
                strList.append( prevStr + toDigit(string) )
            strList.append( prevStr + string ) 
            return strList
        # recursive case, only splits if char can be changed to digit
        if string[0] in dMap:
            # take care of case where char == B, branch for both "b" and "B"
            if string[0] == "B": # create branch for "b" -> "6"
                recHelper(prevStr + "6", string[1:], strList)
            recHelper(prevStr + toDigit(string[0]), string[1:], strList)
        recHelper(prevStr + string[0], string[1:], strList)
    # call helper function on strList
    recHelper("", str, strList)
    return strList


def check_pass(plain,enc):
    """Check to see if the plaintext plain encrypts to the encrypted
       text enc, returns True or False"""
    return crypt.crypt(plain, enc[0:2]) == enc

def load_passwd(filename):
    """Load the password file filename and returns a list of
       dictionaries with fields "account", "password", "UID", "GID",
       "GECOS", "directory", and "shell", each mapping to the
       corresponding field of the file."""
    dictList = []
    dictKeys = ["account","password","UID","GID","GECOS","directories","shell"]
    f = open(filename, 'r')
    text = f.read()
    f.close()
    lines = text.split('\n')
    for l in lines:
        if l != '':
            elems = l.split(':')
            dictList.append( make_dict(dictKeys, elems) )
    return dictList

def crack_pass_file(fn_pass,words,out):
    """Crack as many passwords in file fn_pass as possible using words
       in the file words"""
    #load files
    encryptedPasswords = load_passwd(fn_pass) # dictionary of fields
    words = load_words(words, r"\w{6,8}$") #matches 6 to 8 alphanumeric chars
    crackedPasswords = [] 
    outputFile = open(out, 'w') # file to write cracked passwords to
    # crack untransformed strings first
    for d in encryptedPasswords:
        for w in words:
            if( check_pass(w, d['password']) ): # write "username=pass"
                outputFile.write( '{}={}\n'.format(d['account'], w) )
                encryptedPasswords.remove( d ) #remove entry from future cracks
                outputFile.flush() # output file flushed after each line
    # crack reversed words next in the smaller list of dictionaries
    for d in encryptedPasswords: 
        for w in words:
            if( check_pass( transform_reverse(w)[1], d['password'] ) ): 
                outputFile.write( '{}={}\n'.format(d['account'], w) )
                encryptedPasswords.remove( d ) 
                outputFile.flush()
    # crack words with some letters capitalized
    for d in encryptedPasswords: 
        for w in words:
            capWords = transform_capitalize(w)
            capWords.pop() # last item in list is original word
            for cw in capWords:
                if( check_pass( cw, d['password'] ) ): 
                    outputFile.write( '{}={}\n'.format(d['account'], cw) )
                    encryptedPasswords.remove( d ) 
                    outputFile.flush() 
    # crack words with some letters transformed to digits
    for d in encryptedPasswords: 
        for w in words:
            digitWords = transform_digits(w)
            digitWords.pop() # last item in list is original word
            for dw in digitWords:
                if( check_pass( dw, d['password'] ) ): 
                    outputFile.write( '{}={}\n'.format(d['account'], dw) )
                    encryptedPasswords.remove( d ) 
                    outputFile.flush() 
    # crack words with some letters transformed to caps, some trans'd to digits
    # then check the reversed version of those transformed words
    #transWords = []
    #for d in encryptedPasswords: 
    #    for w in words:
    #        digitWords = transform_digits(w)
    #        digitWords.pop() # last item in list is original word
    #        for dw in digitWords:
    #            capsDigitWords = transform_capitalize(dw)
    #            transWords += capsDigitWords #store all
    #            for cdw in capsDigitWords:
    #                if( check_pass( cdw, d['password'] ) ): 
    #                    outputFile.write( '{}={}\n'.format(d['account'], cdw) )
    #                    encryptedPasswords.remove( d ) 
    #                    outputFile.flush()
    #                # check reversed version of capsDigitWord
    #                cdrw = transform_reverse(cdw)[1]
    #                if( check_pass( cdrw, d['password'] ) ): 
    #                    outputFile.write( '{}={}\n'.format(d['account'], cdrw))
    #                    encryptedPasswords.remove( d ) 
    #                    outputFile.flush() 
    for w in words:
        digitWords = transform_digits(w)
        digitWords.pop() # last item in list is original word
        for dw in digitWords:
            capsDigitWords = transform_capitalize(dw)
            for cdw in capsDigitWords:
                cdRw = transform_reverse(cdw)[1]
                # check unreversed capsDigitWords
                for d in encryptedPasswords:
                   if( check_pass( cdw, d['password'] ) ): 
                       outputFile.write( '{}={}\n'.format(d['account'], cdw) )
                       encryptedPasswords.remove( d ) 
                       outputFile.flush() 
                # check reversed capsDigitWords
                for d in encryptedPasswords:
                   if( check_pass( cdRw, d['password'] ) ): 
                       outputFile.write( '{}={}\n'.format(d['account'], cdRw) )
                       encryptedPasswords.remove( d ) 
                       outputFile.flush()             
    # crack the reversed versions of the previous capsDigitWords
    #for d in encryptedPasswords: 
    #    for w in words:
    #        rw = transform_reverse( w )[1] # reverse the word
    #        digitReversedWords = transform_digits( rw )
    #        digitReversedWords.pop() # last item in list is plain reversed word
    #        for drw in digitReversedWords:
    #            capsDigitReversedWords = transform_capitalize(drw)
    #            for cdrw in capsDigitReversedWords:
    #                if( check_pass( cdrw, d['password'] ) ): 
    #                    outputFile.write( '{}={}\n'.format(d['account'],cdrw) )
    #                encryptedPasswords.remove( d ) 
    #                outputFile.flush()
    # End crack_pass function
    outputFile.close()

    


