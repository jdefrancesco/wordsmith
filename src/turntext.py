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
# Modified: July 12, 2011 @ 4:15 PM
#
# Wordnik API Key: d5a58307aef66a63651080454b601a8f235f7445be04adcba

#!/usr/bin/env python

# Modules to import
from wordnik import * # Turntext is built on the wordnik API
from termcolor import colored, cprint
import enchant # needed for spell checking
import textwrap

import simplejson as json
import sys
import getopt
import logging

# Logging and stuff....
class LogConstants(object):
    LOG_FILENAME = "turntext.log"
    LOG_FORMAT = "%(asctime)s:line number %(lineno)s:%(levelname)s - %(message)s"
    LEVELS = { 'debug' : logging.DEBUG,
                'info' : logging.INFO,
                'warning' : logging.WARNING,
                'error' : logging.ERROR,
                'critical' : logging.CRITICAL}

LOG_SWITCH = True
logfile_name = LogConstants.LOG_FILENAME
log_level = LogConstants.LEVELS.get(logfile_name, logging.NOTSET)
logging.basicConfig(filename=logfile_name, level=log_level, format=LogConstants.LOG_FORMAT)
# End Logging code

# DEFINES - WILL MOVE TO SEPERATE MODULE
DEFAULT_DEFINITION_COUNT = 2
DEFAULT_EXAMPLE_COUNT = 1
# Maximum amount of defintions and examples that can be retrieved (subject to change)
MAX_DEFINITION_COUNT = 5
MAX_EXAMPLE_COUNT = 5

def show_help(): 

    print """
    python turntext.py [FLAGS] [WORD_TO_DEFINE]
        w - Display word of day.
        r - Output a single random word (fun to learn new words)
        l - Output a random list of words
        d - Number of definitions to display
            for a single word. If not supplied the definition
            count will be one.
        e - number of examples to display using supplied word.
            If not supplied the example count will be two.

        *NOTE* flags should always come BEFORE the word you wish to define
    """

# Functions:  p_error(errStr), errStr will be set to a default message if not supplied
# Description: prints out error string and exits
def p_error(errStr):

    # if no error string, set default message
    if not errStr: errStr = "[!] Error, program exiting"
    print errStr
    sys.exit(1)

# Function: nl(count), argument count defaults to one
# Description: Prints new lines. Takes one parameter COUNT, the number of blank lines to output.
def nl(count=1):

    i = 0
    while i < count:
        print ""
        i += 1

# wraps a string for nice output to terminal
def wrap_string(textString): 
    output = textwrap.wrap(textString, 60)
    textString = '\n\t'.join(output)
    return textString

# Function: print_definitions(defList)
# Description: prints out numbered definitions
# Arguments: function takes a single list of definitions
def print_definitions(defList): 

    count = 1
    for definition in defList:
        definition = wrap_string(definition)
        print '\t',str(count) + ". ",  definition
        count += 1


def print_examples(exampList): 
    
    count = 1
    for ex in exampList: 
        example = wrap_string(ex['text'])
        print '\t', str(count), ". ", example
        count += 1


# Function: display_word_info(targetWord, definitions, pronunciation, examples)
def display_word_info(targetWord, definitions, pronunciation, examples):


    if LOG_SWITCH: logging.info('Function: display_word_info()')

    if not len(definitions):
        p_error('[!] ERROR: no definitions available')
    if not len(examples):
        p_error('[!] ERROR: no examples available')


    # defList will hold only the definitions of the word. 
    # Currently the variable 'definitions' has other fields
    
    # Variable 'definitions' is a list of dictionaries with the following six fields
    #  -- word, sequence, text, score, partOfSpeech, sourceDictionary
    defList = []
    posList = [] # part of speech list
    for entry in definitions:
        defList.append(entry['text'])
        posList.append(entry['text'])


    # pronunciation not available for some words ex. mongering
    if(pronunciation): 
        pronounced = pronunciation[0]['raw']
    else:
        pronounced = 'NONE'
    
    # output - word being defined and pronunciation
    print '\n  ', colored(targetWord, 'green', attrs=['bold']), ' ', colored(pronounced, 'yellow')
    print '\n' # new line for neatness

    # prints actual definitions
    print_definitions(defList)

    print ""
    print colored('   Examples', 'red')
    print ""

    # The word_get_examples() function called in fetch_word_info()
    # Also returns a dictionary where we may not use all of the information provided.
    # As a result exampList will contain only the example sentences needed.
    print_examples(examples['examples'])
    
    nl()

    if LOG_SWITCH: logging.info('End: display_word_info() ')
    
# Function: fetch_word_info(wordObj, targetWord, definitionCount, exampleCount)
# Description: Fetches word defintion along with example uses using the Wordnik API
def fetch_word_info(wordObj, targetWord, definitionCount, exampleCount): 
    
    logging.info('Function: fetch_word_info() ')
    if not (0 < definitionCount <= MAX_DEFINITION_COUNT):
        print 'Definition count is out of range, defaulting to', DEFAULT_DEFINITION_COUNT
        definitionCount = DEFAULT_DEFINITION_COUNT

    if not (0 < exampleCount <= MAX_EXAMPLE_COUNT):
        print 'Example count is out of range, defaulting to', DEFAULT_EXAMPLE_COUNT
        exampleCount = DEFAULT_EXAMPLE_COUNT


    # Spell checking and correction options, SOME WORDS ARE NOT IN ENCHANT DICT
    spellCheck = enchant.Dict('en_US')
    if not spellCheck.check(targetWord):
        print 'tmp: Show alternatives'
        print spellCheck.suggest(targetWord)

    # Wordnik API calls made here.. See wordnik documentation for any details regarding arguments
    # note: 'definitions' variable will contain a LIST, and 'examples' will be a DICT
    definitions = wordObj.word_get_definitions(targetWord, limit=definitionCount)
    pronunciation = wordObj.word_get_pronunciations(targetWord, typeFormat='ahd') 
    examples = wordObj.word_get_examples(targetWord, limit=exampleCount)

    logging.info('End: fetch_word_info()')
    return (definitions, pronunciation, examples)


# word_of_day() - Display word of the day and its definition
# Arguments: Wordnik object
def get_word_of_day(word):

    # Wordnik API returns JSON data
    # function returns a dictionary
     ret = word.words_get_word_of_the_day()
     targetWord = ret['word'] # just fetch the word, call fetch_word_info and display

     # make calls for word of day and display result
     definitions, pronunciation, examples = fetch_word_info(word, targetWord, DEFAULT_DEFINITION_COUNT, DEFAULT_EXAMPLE_COUNT)
     display_word_info(targetWord, definitions, pronunciation, examples)
     
     
# return list of random words
def get_random_list(): pass

# return one random word
def get_random_word(): pass

def main():

    logging.info('\n\nmain() called - program started') # remove eventually
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
        if o == '-w': # implemented 
            if LOG_SWITCH: logging.info('[+] Word of day switch on. (-w)')
            get_word_of_day(word)

        elif o == '-r': # get random word
            if LOG_SWITCH: logging.info('[+] Get random word switch on. (-r)')
            get_random_word()

        elif o == '-l': # get random list of words
            if LOG_SWITCH: logging.info('[+] Get random list of words switch on. (-l)')
            get_random_list() 

        elif o == '-d': # implemented
            if LOG_SWITCH: logging.info('[+] Definition count switch on. (-d)')
            if int(a) != DEFAULT_DEFINITION_COUNT: 
                definitionCount = int(a)

        elif o == '-e': #implemented
            if LOG_SWITCH: logging.info('[+] Examples count switch on. (-e)')
            if int(a) != DEFAULT_EXAMPLE_COUNT: 
                exampleCount = int(a)
        else:
            logging.warning('Invalid flag provided')
            print "Invalid flag <== show help"

    if len(args) == 0:
        p_error('[!] Error: No word was given to lookup')

    # target word to define is our first (and only for now) element in args list
    targetWord = args[0]

    definitions, pronunciation, examples = fetch_word_info(word, targetWord, definitionCount, exampleCount)
    display_word_info(targetWord, definitions, pronunciation, examples)

    logging.info('**END**')
    #END

# Handles command line arguments, then call main()
if __name__ == '__main__':
    main()
