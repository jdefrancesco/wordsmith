#!/usr/bin/env python

from wordnik import *
import simplejson

# WORDNIK API KEY: d5a58307aef66a63651080454b601a8f235f7445be04adcba

# wordnik test

# Note: Key isn't validated until first call is made
word = Wordnik('d5a58307aef66a63651080454b601a8f235f7445be04adcba');


# Parameters - See: http://developer.wordnik.com/docs/ 

# JASON RETURN Fields
# {word ,sequence, text, score, partOfSpeech, sourceDictionary}
myWord = 'augment'




# Definitions
returnQuery = word.word_get_definitions(myWord)
for i in returnQuery:
    print i['word'], " : ", i['text']


# Related words
word.word_get_related()

# Example sentences
word.word_get_examples() # get examples
word.word_get_top_example() # only get the best rated example

# Tool - get word of the day
word.words_get_word_of_the_day() # word of day utility feature


word.word_get_random_word() # get single random word
word.word_get_random_words() # list of specified random words

