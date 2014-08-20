# from contratest.models import *
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
        newstring = re.search('(?<=[AB][12]: ).*', element).group()
        newlist.append(newstring.split("; "))

    return newlist

def make_move(move_string, dance):
    return Move



def get_movename(move_string):
    pass

text = file_to_string("babyrose.txt")
dance_list = break_input(text)
dance = make_dance(dance_list[0])
clean_moves = clean_moves_list(dance_list[1:])

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


