# TurnText - A swiss army knife for working with words 
# 
# Distributed under LGPL (http://www.gnu.org/copyleft/lesser.html)
# Written by : Joey DeFrancesco
# Modified: May 11, 2011 @ 2:21PM
#
# Note: TurnText relies heavily on wordnik's api and python library.
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

def showHelp(): 

    
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
        w - word of day
        r - random list of words
        d - number of definitions to display
            for a single word. Defaults to 2
            of the top rated definitions.
    """

# word_of_day() - Display word of the day
# ARGS: Wordnik object
def word_of_day(word):

    # Wordnik API returns JSON data
    # function returns a dictionary
    words = word.words_get_word_of_the_day()
   
    # NOTE: TEMPORARY TESTING OUTPUT UNTILL 
    #       I WRITE FORMATTING AND DISPLAY
    #       FUNCTIONS.

    for key, val in words.iteritems():
        print key, '=>', val
    # we exit, as we only want word of the day.
    sys.exit(0)

def get_random_list(): pass
def get_random_word(): pass

def main():

    if len(sys.argv) < 2:
        showHelp()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'wrld:e: ')
    except getopt.GetoptError, err:
        # help information, then exit
        print str(err)
        showHelp()
        sys.exit(1)

    # Create Wordnik object, Authenticate with API key (See header comment block)
    word = Wordnik('d5a58307aef66a63651080454b601a8f235f7445be04adcba')
    # Handle our options

    # Number of definitions and examples to show (Default)
    definitionCount = DEFAULT_DEFINITION_COUNT
    exampleCount = DEFAULT_EXAMPLE_COUNT
    
    for o, a in opts:
        if o == '-w': # display word of the day, then exit.
            word_of_day(word)
            # single option - exit
        elif o == '-r': # get random word
            
            # single option - exit
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

# Handles command line arguments, then call main()
if __name__ == '__main__':
    main()
