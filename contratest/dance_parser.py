from contratest.models import Dance, Move
import re

# break into lines
# get metadata from line 1
# individual lines, break into sub-lists (split on ;)
# sect, seq automatically
# lowercase

def parse_dance(filename):
    text = file_to_string("contratest/babyrose.txt")
    dance_list = break_input(text)
    dance = make_dance(dance_list[0])
    dance.save()
    clean_moves = clean_moves_list(dance_list[1:])
    make_all_moves(clean_moves_list, dance)

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
    return Dance(title=title, author=author, formation=formation)

def clean_moves_list(moves_list):
    newlist = []
    for element in moves_list:

        newstring = re.search('(?<=[ab][12]: ).*', element.lower()).group()
        newlist.append(newstring.split("; "))

    return newlist

def make_move(move_string, dance, sect_no, seq_no):
    new_move = Move(dance=dance, seq=seq_no, sect=sect_dict[sect_no])
    new_move.movename = get_movename(move_string)
    for attr in expected_values[new_move.movename]:
        setattr(new_move, attr, functions[attr](move_string, new_move.movename))
    return new_move

def make_all_moves(moves_list, dance):
    sect_counter = 1
    move_counter = 1
    for sect_list in moves_list:
        for move in sect_list:
            dance.move_set.add(make_move(move, dance, sect_counter, move_counter))
            move_counter += 1
        sect_counter +=1


def get_movename(move_string):
    attempt = get_any(move_string, movename_dict)
    if attempt:
        return attempt
    else:
        return raw_input("I can't tell; what move is this?\n(Input was: %s)\n>" % move_string)

def get_bal(move_string, movename):
    attempt = get_any(move_string, bal_dict)
    if attempt:
        return attempt
    else:
        return False

def get_dir(move_string, movename):
    if movename in ["circle"]:
        attempt = get_any(move_string, dir_dict_simple)
        default = "L"
    elif movename in ["promenade", "rlthru", "chain"]:
        attempt = get_any(move_string, dir_dict_complex)
        default = "across"
    if attempt:
        return attempt
    else:
        return default

def get_dist(move_string, movename):
    if movename in ["circle", "star"]:
        attempt = get_any(move_string, dist_dict_simple)
        default = 4
    elif movename in ["allemande", "dosido", "gypsy", "seesaw"]:
        attempt = get_any(move_string, dist_dict_complex)
        default = None
    if attempt:
        return attempt
    else:
        return default

def get_who(move_string, movename):
    attempt = get_any(move_string, who_dict)
    if attempt:
        return attempt
    else:
        if movename in ["chain"]:
            return "ladies"
        else:
            return raw_input("I can't tell; what is the value of 'who'?\n(Input was: %s)\n>" % move_string)

def get_hand(move_string, movename):
    attempt = get_any(move_string, hand_dict)
    if attempt:
        return attempt
    else:
        return raw_input("I can't tell; what is the value of 'hand'?\n(Input was: %s)\n>" % move_string)

def get_hands_across(move_string, movename):
    attempt = get_any(move_string, hands_across_dict)
    if attempt:
        return attempt
    else:
        return None #...should this return false instead?


def get_any(move_string, dict):
    for key in dict.keys():
        if move_string.find(key) > -1:
            return dict[key]
    else:
        return

text = file_to_string("contratest/babyrose.txt")
dance_list = break_input(text)
dance = make_dance(dance_list[0])
clean_moves = clean_moves_list(dance_list[1:])

sect_dict = {
    1: "A1",
    2: "A2",
    3: "B1",
    4: "B2"
}

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

bal_dict = {
    "b&s": True,
    "bal": True,
    "no bal": False
}

dist_dict_simple = {
    "1 place": 1,
    "2 place": 2,
    "3 place": 3,
    "4 place": 4,
    "5 place": 5,
    "6 place": 6,
    "1x": 4,
    "once": 4,
    "half": 2,
    "1 1/4": 5,
    "1 1/2": 6, #this won't ever ping b/c 1/2 is in dict too
    "1/2": 2,
    "3/4": 3
    # what about 3/4 as unicode fract, etc.?
}

dist_dict_complex = {
    "1x": 1,
    "3/4": 0.75, #assuming I'll never see a 1 3/4 alle<FIX THIS!
    "1 1/4": 1.25,
    "1 1/2": 1.5, #assuming I'll never see just a half alle
    "once": 1,
    "1.5": 1.5,
    "1.5": 1.5

}

dir_dict_simple = {
    " l ": "L",
    "left": "L",
    " r ": "R",
    "right": "R"
}

dir_dict_complex = {
    "across": "across",
    "l diag": "ldiag",
    "ldiag": "ldiag",
    "r diag": "rdiag",
    "rdiag": "rdiag"
}

hand_dict = {
    " l ": "L",
    "left": "L",
    "lh": "L",
    " r ": "R",
    "right": "R",
    "rh": "R"
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

hands_across_dict = {
    "hands across": True,
    "hands-across": True
}

# list of what values each move expects
expected_values = {
    "swing": ["who", "bal"],
    "circle": ["dir", "dist"],
    "star": ["hand", "dist", "hands_across"],
    "dosido": ["who", "dist"],
    "chain": ["who", "dir"],
    "longlines": ["rollaway"],
    "allemande": ["who", "hand", "dist"],
    "seesaw": ["who", "dist"],
    "hey": ["who", "hand", "hey_length", "ricochet"],
    "gypsy": ["who", "hand", "dist"],
    "rlthru": ["dir"],
    "petronella": [],
    "pass_ocean": [],
    "yearn": [],
    "wave": ["wave_length"],
    "give_take": [],
    "promenade": ["dir"],
    "down_hall": ["turn_how"],
    "other": []}

dicts_by_attr = {
    "movename": movename_dict,
    "who": who_dict,
    "bal": bal_dict,
}

functions = {
    "who": get_who,
    "bal": get_bal,
    "dir": get_dir,
    "dist": get_dist,
    "hand": get_hand,
    "hands_across": get_hands_across
}
# http://www.cotellese.net/2007/09/27/running-external-scripts-against-django-models/
