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
from wordnik import *

import simplejson as json
import sys
import getopt
import logging

class LogConstants(object):
    LOG_FILENAME = ""
    LOG_FORMAT = "%(asctime)s:line number %(lineno)s:%(levelname)s - %(message)s"
    LEVELS = { 'debug' : logging.DEBUG,
                'info' : logging.INFO,
                'warning' : logging.WARNING,
                'error' : logging.ERROR,
                'critical' : logging.CRITICAL}

# Wordnik API Key: d5a58307aef66a63651080454b601a8f235f7445be04adcba

# DEFINES - MOVE TO SEPERATE MODULE
DEFAULT_DEFINITION_COUNT = 2
DEFAULT_EXAMPLE_COUNT = 1


def DEBUG(): print '***DEBUG***'

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

# Function: define_word(targetWord, definitionCount, exampleCount)
# In: target word, number of definitions to return, 
# Out: 
# Description: Fetches word defintion along with example uses using the Wordnik API
define_word(): pass

# word_of_day() - Display word of the day and its definition
# Arguments: Wordnik object
# NOTE: Function exits program.
def word_of_day(word):

    # Wordnik API returns JSON data
    # function returns a dictionary
    words = word.words_get_word_of_the_day()
   
    # NOTE: TEMPORARY TESTING OUTPUT UNTILL 
    #       I WRITE FORMATTING AND DISPLAY
    #       FUNCTIONS.

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
            get_word_of_day(word)

        elif o == '-r': # get random word
            get_random_word()

        elif o == '-l': # get random list of words
            get_random_list()  

        elif o == '-d':
            # MAKE SURE THEY SUPPLY NUMBER (RESTRICT 10)
            # Specify how many definitions to display
            if int(a) != DEFAULT_DEFINITION_COUNT: 
                definitionCount = int(a)
        elif o == '-e':
            # CHECK IF NUMBER IS GIVEN (RESTRICT 10)
            # Specify how many examples to display
            if int(a) != DEFAULT_EXAMPLE_COUNT: 
                exampleCount = int(a)
        else:
            print "Invalid flag <== show help"

    if len(args) == 0:
        return 0 # no word was supplied to be defined

    # target word to define is our first (and only for now) element in args list
    targetWord = args[0]

    define_word(targetWord, definitionCount, exampleCount)

# Handles command line arguments, then call main()
if __name__ == '__main__':
    main()
