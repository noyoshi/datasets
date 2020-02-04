#!/usr/bin/env python3
# Copywrite Sam "Big Shot" Battalio
# General structure / Regex modified from @Author yohanes.gultom@gmail

import re
import sys

# Globals

# single word type pattern
START_PATTERN      = re.compile(r'^(.*?)<ENAMEX$', re.I)
END_SINGLE_PATTERN = re.compile(r'^TYPE="(.*?)">(.*?)</ENAMEX>(.*?)$', re.I)
# multi word pattern
TYPE_PATTERN       = re.compile(r'^TYPE="(.*?)">(.*?)$', re.I)
END_MULTI_PATTERN  = re.compile(r'^(.*?)</ENAMEX>(.*?)$', re.I)
EOS_PATTERN        = re.compile(r'^([^<>]*)\.?\t(\d+)$', re.I)

# check regular word for punctuation
WRAP_PUNC_PATTERN  = re.compile(r'^([.,\(\)]"?!)([^.,\)\("?!]+)([.,\(\)"?!])$', re.I)
START_PUNC_PATTERN = re.compile(r'^([.,\(\)"?!])(.+)$', re.I)
END_PUNC_PATTERN   = re.compile(r'^(.+)([.,\(\)"?!])$', re.I)

PUNCTUATION = ',.()\'&-'

NON_ENTITY_TYPE = 'O'

# Functions

def handle_end_of_string(token, curr_type):
    ''' checks & handles end of statement '''
    match = re.match(EOS_PATTERN, token)
    if match:
        return match.group(1) + '\t' + curr_type + '\n.\t' + curr_type + '\n'
    return None

def get_lines(file_name):
    ''' reads file and returns generator '''
    with open(file_name, 'r') as f:
        for line in f:
            yield line

def determine_type(type_string, is_beginning):
    if type_string == NON_ENTITY_TYPE:
        return NON_ENTITY_TYPE
    elif is_beginning:
        return type_string + '-B'
    else:
        return type_string + '-I'

def space_out_characters(string, characters):
    ''' returns string with more easily consumable punctuation (spaced out) '''
    for char in characters:
        string = string.replace(char, ' ' + char + ' ')

    return string

# Main Execution

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('{} FILENAME'.format(sys.argv[0]))
        sys.exit(1)

    out_string = ""
    curr_type  = NON_ENTITY_TYPE

    for sentence in get_lines(sys.argv[1]):
        out_string += sentence
        sentence = space_out_characters(sentence, PUNCTUATION)
        # basically check if each token is normal or like the start or end of tag
        for token in sentence.split('\t')[0].split():
            # grab garbage start of tag and any token before
            match = re.match(START_PATTERN, token)
            if match:
                if match.group(1):
                    out_string += match.group(1) + '\t' + NON_ENTITY_TYPE + '\n'
                continue
            
            # typeregex and end of tag 
            match = re.match(END_SINGLE_PATTERN, token)
            if match:
                # write out the thing & type
                out_string += match.group(2) + '\t' + determine_type(match.group(1), True) + '\n'
                curr_type = NON_ENTITY_TYPE
                is_beginning = True # reset
                checked   = handle_end_of_string(match.group(3), determine_type(curr_type, False))
                if not checked:
                    if match.group(3):
                        out_string += match.group(3) + '\t' + determine_type(curr_type, False) + '\n'
                else:
                    out_string += checked
                continue

            # handle multiword type front
            match = re.match(TYPE_PATTERN, token)
            if match:
                curr_type = match.group(1)
                out_string += match.group(2) + '\t' + determine_type(curr_type, True) + '\n'
                continue

            # handle end of multiword
            match = re.match(END_MULTI_PATTERN, token)
            if match:
                out_string += match.group(1) + '\t' + determine_type(curr_type, False) + '\n'
                curr_type = NON_ENTITY_TYPE
                is_beginning = True # reset beginning mark
                checked = handle_end_of_string(match.group(2), determine_type(curr_type, False)) 
                if not checked:
                    if match.group(2):
                        out_string += match.group(2) + '\t' + determine_type(curr_type, False) + '\n'
                else:
                    out_string += checked
                continue

            # check paren on both sides
            match = re.match(WRAP_PUNC_PATTERN, token)
            if match:
                out_string += match.group(1) + '\t' + determine_type(curr_type, False) + '\n'
                out_string += match.group(2) + '\t' + determine_type(curr_type, False) + '\n'
                out_string += match.group(3) + '\t' + determine_type(curr_type, False) + '\n'
                break

            # check regular token for punctuation in front
            match = re.match(START_PUNC_PATTERN, token)
            if match:
                out_string += match.group(1) + '\t' + determine_type(curr_type, False) + '\n'
                out_string += match.group(2) + '\t' + determine_type(curr_type, False) + '\n'
                continue
 
            match = re.match(END_PUNC_PATTERN, token)
            if match: 
                out_string += match.group(1) + '\t' + determine_type(curr_type, False) + '\n'
                out_string += match.group(2) + '\t' + determine_type(curr_type, False) + '\n'
                continue

            checked = handle_end_of_string(token, determine_type(curr_type, False))
            if checked:
                out_string += checked
                continue

            out_string += token + '\t' + determine_type(curr_type, False) + '\n'
             
        out_string += '\n'

    print(out_string)
