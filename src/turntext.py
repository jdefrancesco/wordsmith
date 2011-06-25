# TurnText - A swiss army knife for working with words 
# 
# Description: TurnText aims to be a simple, light-weight command line dictionary/word
#              utility. TurnText will clean and efficient, delivering high quality
#              definitions and examples for any word you would like the meaning of.
#               
#              TurnText relies heavily on (and may in some sense be a wrapper) the Worknik API.
#              The use of WordNik allows for quality definitions and examples as well as other
#              features you may find useful.
#
# Distributed: LGPL (http://www.gnu.org/copyleft/lesser.html)
# Written by : Joey DeFrancesco
# Modified: May 24, 2011 @ 11:52 PM
#
# Wordnik API Key: d5a58307aef66a63651080454b601a8f235f7445be04adcba

#!/usr/bin/env python

# Modules to import
from wordnik import * # Turntext is built on the wordnik API
from termcolor import colored, cprint
import enchant # needed for spell checking

import simplejson as json
import sys
import getopt
import logging

# Logging and stuff....
class LogConstants(object):
    LOG_FILENAME = "turntext.py"
    LOG_FORMAT = "%(asctime)s:line number %(lineno)s:%(levelname)s - %(message)s"
    LEVELS = { 'debug' : logging.DEBUG,
                'info' : logging.INFO,
                'warning' : logging.WARNING,
                'error' : logging.ERROR,
                'critical' : logging.CRITICAL}

LOG_SWITCH = True
level_name = LogConstants.LOG_FILENAME
log_level = LogConstants.LEVELS.get('turntext_log.txt', logging.NOTSET)
logging.basicConfig(filename=LogConstants.LOG_FILENAME, level=log_level, format=LogConstants.LOG_FORMAT)
# End Logging code

# DEFINES - WILL MOVE TO SEPERATE MODULE
DEFAULT_DEFINITION_COUNT = 2
DEFAULT_EXAMPLE_COUNT = 1
# Maximum amount of defintions and examples that can be retrieved (subject to change)
MAX_DEFINITION_COUNT = 5
MAX_EXAMPLE_COUNT = 5

def show_help(): 

    
    # parse arguments, optlist contains flags and corresponding options.
    # args becomes a list of single arguments passed to the program.
    # Argument Line: w -- word of the day
    #                r -- ramdom word
    #                l -- random list of words
    #                d -- number of definitions (Default = 2)
    #                e -- number of examples

    # TEMPORARY FOR TESTING
    print """
    python turntext.py [ARGS]
        w - display word of day
        r - output a single random word (fun to learn new words)
        l - output a random list of words
        d - number of definitions to display
            for a single word. Defaults to 2
            of the top rated definitions.
    """


# Function: display_word_info(definitions, examples)
def display_word_info(targetWord, definitions, pronounciation, examples):


    if not len(definitions):
        print 'Error -- definition count invalid' # tmp handling
        return

    if not len(examples):
        print 'Error -- examples count invalid' # tmp handling
        return 

    # defList will hold only the definitions of the word. 
    # Currently the variable 'definitions' has other fields
    
    # Variable 'definitions' is a list of dictionaries with the following six fields
    #  -- word, sequence, text, score, partOfSpeech, sourceDictionary

    # using to parallel lists for simplicity sake
    defList = []
    posList = [] # part of speech list
    for entry in definitions:
        defList.append(entry['text'])
        posList.append(entry['text'])


    # output (to be made way nicer) TESTING ONE TWO START HERE DEAZY!
    print targetWord, '  ', pronunciation[0]['raw']


# Function: fetch_word_info(wordObj, targetWord, definitionCount, exampleCount)
# In: 
# Out: 
# Description: Fetches word defintion along with example uses using the Wordnik API
def fetch_word_info(wordObj, targetWord, definitionCount, exampleCount): 
  
    if not (0 < definitionCount <= MAX_DEFINITION_COUNT):
        print ' error -- exiting ' # temporary action 
        sys.exit(1)

    if not (0 < exampleCount <= MAX_EXAMPLE_COUNT):
        print 'error example count invalid -- exiting' # temporary action
        sys.exit(1) 

    # Spell checking and correction options
    spellCheck = enchant.Dict('en_US')
    if not spellCheck.check(targetWord):
        # TODO: allow user to chose alternative word
        print 'tmp: Show alternatives'
        print spellCheck.suggest(targetWord)

    # Wordnik API calls made here.. See wordnik documentation for any details regarding arguments
    # note: 'definitions' variable will contain a LIST, and 'examples' will be a DICT
    definitions = wordObj.word_get_definitions(targetWord, limit=definitionCount)
    pronunciation = word.word_get_pronunciations(targetWord, typeFormat=ahd) 
    examples = wordObj.word_get_examples(targetWord, limit=exampleCount)

    return (definitions, pronunciation, examples)


# word_of_day() - Display word of the day and its definition
# Arguments: Wordnik object
def word_of_day(word):

    # Wordnik API returns JSON data
    # function returns a dictionary
    words = word.words_get_word_of_the_day()
   

    for key, val in words.iteritems():
        print key, '=>', val

# return list of random words
def get_random_list(): pass

# return one random word
def get_random_word(): pass

def main():

    if len(sys.argv) < 2:
        show_help()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'wrld:e: ')
    except getopt.GetoptError, err:
        # help information, then exit
        print str(err)
        show_help()
        sys.exit(1)

    # Create Wordnik object, Authenticate with API key (See header comment block)
    word = Wordnik('d5a58307aef66a63651080454b601a8f235f7445be04adcba')
    # Handle our options

    # Number of definitions and examples to show (Default)
    definitionCount = DEFAULT_DEFINITION_COUNT
    exampleCount = DEFAULT_EXAMPLE_COUNT

    for o, a in opts:
        if o == '-w': # display word of the day, then exit.
            if LOG_SWITCH: logging.info('[+] Word of day switch on. (-w)')
            get_word_of_day(word)

        elif o == '-r': # get random word
            if LOG_SWITCH: logging.info('[+] Get random word switch on. (-r)')
            get_random_word()

        elif o == '-l': # get random list of words
            if LOG_SWITCH: logging.info('[+] Get random list of words switch on. (-l)')
            get_random_list() 

        elif o == '-d':
            if LOG_SWITCH: logging.info('[+] Definition count switch on. (-d)')
            # MAKE SURE THEY SUPPLY NUMBER (RESTRICT 10)
            # Specify how many definitions to display
            if int(a) != DEFAULT_DEFINITION_COUNT: 
                definitionCount = int(a)

        elif o == '-e':
            if LOG_SWITCH: logging.info('[+] Examples count switch on. (-e)')
            # CHECK IF NUMBER IS GIVEN (RESTRICT 10)
            # Specify how many examples to display
            if int(a) != DEFAULT_EXAMPLE_COUNT: 
                exampleCount = int(a)
        else:
            logging.warning('Invalid flag provided')
            print "Invalid flag <== show help"

    if len(args) == 0:
        return 0 # no word was supplied to be defined

    # target word to define is our first (and only for now) element in args list
    targetWord = args[0]
    definitions, pronunciation, examples = fetch_word_info(word, targetWord, definitionCount, exampleCount)
    logging.info('got defintions (LIST), for examples (DICT)')

    display_word_information(targetWord, definitions, pronunciation, examples)

    #END

# Handles command line arguments, then call main()
if __name__ == '__main__':
    main()
