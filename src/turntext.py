# TurnText - A swiss army knife for working with words 
# 
# Distributed under LGPL (http://www.gnu.org/copyleft/lesser.html)
# Written by : Joey DeFrancesco
# Modified: May 11, 2011 @ 2:21PM

#!/usr/bin/env python

# Modules to import
from wordnik import *

import simplejson
import sys
import getopt

# Wordnik API Key: d5a58307aef66a63651080454b601a8f235f7445be04adcba

def DEBUG(): print '***DEBUG***'

def showHelp(): pass

    # parse arguments, optlist contains flags and corresponding options.
    # args becomes a list of single arguments passed to the program.
    # Argument Line: w -- word of the day
    #                r -- ramdom word
    #                l -- random list of words
    #                d -- number of definitions (Default = 2)
    #                e -- number of examples

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'wrld:e: ')
    except getopt.GetoptError, err:
        # help information, then exit
        print str(err)
        showHelp()
        sys.exit(1)
    
    # Handle our options
    for o, a in opts:
        # TODO: --->> LEFT OFF HERE

# Handles command line arguments, then call main()
if __name__ == '__main__':
    main()
