from contratest.models import Dance, Move
import re

# break into lines
# get metadata from line 1
# individual lines, break into sub-lists (split on ;)
# sect, seq automatically
# lowercase

def file_to_string(filename):
    with open(filename) as infile:
        text = infile.read()
    return text

def break_input(input):
    return input.split("\n")

def make_dance(dance_string):
    dance_info = re.search('(.*) by (.*) [(](.*)[)]', dance_string)
    title = dance_info.group(1)
    author = dance_info.group(2)
    formation = dance_info.group(3)
    return {"title": title, "author": author, "formation": formation}

def clean_moves_list(moves_list):
    newlist = []
    for element in moves_list:

        newstring = re.search('(?<=[ab][12]: ).*', element.lower()).group()
        newlist.append(newstring.split("; "))

    return newlist

def make_move(move_string, dance):
    return Move



def get_movename(move_string):
    for key in movename_dict.keys():
        if move_string.find(key) > -1:
            return movename_dict[key]
    else:
        return raw_input("I can't tell; what move is this?\n>")


text = file_to_string("contratest/babyrose.txt")
dance_list = break_input(text)
dance = make_dance(dance_list[0])
#clean_moves = clean_moves_list(dance_list[1:])

movename_dict = {
    "swing": "swing",
    "b&s": "swing",
    "gypsy": "gypsy",
    "dsd": "dosido",
    "dosido": "dosido",
    "do-si-do": "dosido",
    "alle": "allemande",
    "turn by": "allemande", #this is the hardest!
    "star": "star",
    "circle": "circle",
    "long lines": "longlines",
    "f&b": "longlines",
    "ll ": "longlines",
    "chain": "chain",
    "down the hall": "down_hall", #turning must be own move
    "prom": "promenade"
}

who_dict = {
    "ladies": "ladies",
    "woman": "ladies",
    "gents": "gents",
    "men": "men",
    "n ": "neighbor",
    "ns": "neighbor",
    "neighbor": "neighbor",
    "P ": "partner",
    "ps": "partner",
    "partner": "partner",
    "shad": "shadow",
    "shadow": "shadow"
}
'''
# list of what values each move expects
expected_values = {
    "swing": ["who", "bal"],
    "circle": ["dir", "dist"],
    "star": ["hand", "dist", ("hands_across")],
    "dosido": ["who", ("dist")],
    "chain": [("who"), ("dir")],
    "longlines": ["rollaway"],
    "allemande": ["who", "hand", "dist"],
    "seesaw": ["who", "dist"],
    "hey": ["who", "hand", "hey_length", ("ricochet")],
    "gypsy": ["who", "hand", ("dist")],
    "rlthru": [("dir")],
    "petronella": [],
    "pass_ocean": [],
    "yearn": [],
    "wave": ["wave_length"],
    "give_take": [],
    "promenade": [("dir")],
    "down_hall": ["turn_how"],
    "other": []}
    '''

# http://www.cotellese.net/2007/09/27/running-external-scripts-against-django-models/
