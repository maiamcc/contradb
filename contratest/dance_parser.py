from contratest.models import *
import re

def parse_dance(filename):
    """Converts a human-written dance from given
        text file into a Dance object with all
        Move objects, saves in database."""
    text = file_to_string(filename)
    dance_list = break_input(text)
    dance = make_dance(dance_list[0])
    dance.save()
    clean_moves = clean_moves_list(dance_list[1:])
    make_all_moves(clean_moves, dance)
    # when add 'notes' field to dance object, how parse notes?

def file_to_string(filename):
    """Reads a text file containing a dance."""
    with open(filename) as infile:
        text = infile.read()
    return text

def break_input(input):
    """Splits input by new-line."""
    return input.split("\n")

def make_dance(dance_string):
    """Makes a Dance object by parsing the title/author/formation
        information in the first line of the dance."""
    dance_info = re.search('(.*) by (.*) [(](.*)[)]', dance_string)
    title = dance_info.group(1)
    author = dance_info.group(2)
    formation = dance_info.group(3)
    # Missing: progression
    return Dance(title=title, author=author, formation=formation)

def clean_moves_list(moves_list):
    """Given a list containing all of the lines from the dance
        (some of which may contain more than one move), makes a
        nested list of the moves in each section, splitting on ';'"""
    newlist = []
    for element in moves_list:

        newstring = re.search('(?<=[ab][12]: ).*', element.lower()).group()
        newlist.append(newstring.split("; "))

    return newlist

def make_move(move_string, dance, sect_no, seq_no, count=None):
    """Given a string representing a single move, makes a Move
        object. Expects the string, the dance to which the move
        belongs, an int indicating the section (1=A1, 2=A2, etc.)
        and an int indicating place in the dance sequence."""
    new_move = Move(dance=dance, seq=seq_no, sect=sect_dict[sect_no])
    new_move.movename = use_parser(move_string, parse_movename, ask="What's the value of 'movename'?")
    if count:
        new_move.count = count
    else:
        new_move.count = use_parser(move_string, parse_count, default=8)

    for attr in expected_values[new_move.movename]:
        setattr(new_move, attr, parser_lookup(move_string, attr, new_move.movename))

    needs_extra_info = use_parser(move_string, parse_extra, default=False)
    if needs_extra_info:
        new_move = get_extra_info(move_string, new_move)

    return new_move

def make_all_moves(moves_list, dance):
    """Given a nested list of all of the moves in a dance (in lists
        based on section), makes all into Move objects."""
    sect_counter = 1
    move_counter = 1
    for sect_list in moves_list:
        for move in sect_list:
            if len(sect_list) == 1:
                count = 16
            else:
                count = None
            dance.move_set.add(make_move(move, dance, sect_counter, move_counter, count))
            move_counter += 1
        sect_counter +=1

def parser_lookup(input, attr, movename):
    """Returns the result of the appropriate parser (given
        movename and attribute) on the given input.

        This is useful because certain moves will parse certain
            attributes differently, some moves will take different
            defaults than others and some will take no default, etc."""
    if attr == "who":
        if movename != "chain":
            return use_parser(input, parse_who, ask="What's the value of 'who'?")
        else:
            return use_parser(input, parse_who, default="ladies")
    elif attr == "bal":
        return use_parser(input, parse_bal, default="0")
    elif attr == "dir":
        if movename != "chain":
            return use_parser(input, parse_dir, ask="What's the value of 'dir'?")
        else:
            return use_parser(input, parse_dir, default="across")
    elif attr == "dist":
        if movename in ["circle", "star"]:
            return use_parser(input, parse_dist_whole, ask="What's the value of 'dist'? Please input in whole number of places, e.g. 'circle L 3/4' --> '3'.)")
        elif movename == "allemande":
            return use_parser(input, parse_dist_dec, ask="What's the value of 'dist'? Please input as a decimal.")
        elif movename in ["dosido", "gypsy", "seesaw"]:
            return use_parser(input, parse_dist_dec, default=None)
    elif attr == "hand":
        return use_parser(input, parse_hand, ask="What's the value of 'hand'?")
    elif attr == "hands_across":
        return use_parser(input, parse_hands_across, default="0")
    elif attr == "turn_how":
        return use_parser(input, parse_turn_how, ask="What's the value of 'turn_how'? (Accepted values: 'alone', 'couple'.)")
    elif attr == "moreinfo":
        return raw_input("Describe this move.\n(Input was: %s)\n> " % input)
    elif attr == "progress":
        return "" # just for now

# Making parsers
def one_of(parsers, ask=None, default=None):
    def parser(input):
        for p in parsers:
            result = p(input)
            if result:
                return result
    return parser

def use_parser(input, parser, ask=None, default=None):
    result = parser(input)
    if result:
        return result
    elif ask:
        return raw_input(ask + "\n(Input was: %s)\n> " % input)
    else:
        return default

# TODO: check that raw input is valid?

# Count

def parse_count(input):
    m = re.search('\(([1-9]+)\)', input)
    if m:
        return int(m.group(1))
    else:
        return

# Distances

def dist_whole_place(input):
    m = re.search('([1-6]) place', input)
    if m:
        return int(m.group(1))
    else:
        return

def dist_whole_fract(input):
    # should be able to search for unicode fract chars...
    m = re.search('([1-9])/([1-9])', input)
    if m:
        n = re.search('[1-9] [1-9]/[1-9]', input)
        if n:
            if n.group() == "1 1/4":
                return 5
            elif n.group() == "1 1/2":
                return 6
        else:
            if m.group(2) == "4":
                return int(m.group(1))
            elif m.group(1) == "1" and m.group(2) == "2":
                return 2
    else:
        return

def dist_whole_text(input):
    if "once" in input:
        return 4
    elif "half" in input:
        return 2
    elif "all the way" in input:
        return 4
    elif "1x" in input:
        return 4
    else:
        return

dist_whole_parserlist = [dist_whole_place, dist_whole_fract, dist_whole_text]
parse_dist_whole = one_of(dist_whole_parserlist)

def dist_dec_fract(input):
    # should be able to search for unicode fract chars...
    m = re.search('([1-9])/([1-9])', input)
    if m:
        result = ""
        n = re.search('([1-9]) [1-9]/[1-9]', input)
        if n:
            result += n.group(1)

        if m.group(1) == "1" and m.group(2) == "2":
            result += ".5"
        elif m.group(2) == "4":
            if m.group(1) == "1":
                result += ".25"

            elif m.group(1) == "3":
                result += ".75"

        return float(result)
    else:
        return

def dist_dec_text(input):
    if re.search('once.*half', input):
        return 1.5
    elif "once" in input:
        return 1
    elif "1x" in input:
        return 1
    elif "half" in input:
        return 0.5
    else:
        return

def dist_dec_decimal(input):
    m = re.search('[1-9]\.[1-9]', input)
    if m:
        return float(m.group())
    else:
        return

dist_dec_parserlist = [dist_dec_fract, dist_dec_text, dist_dec_decimal]
parse_dist_dec = one_of(dist_dec_parserlist)

def parse_movename(input):
    attempt = get_any(input, movename_dict)
    if attempt:
        return attempt
    else:
        return

def parse_bal(input):
    attempt = get_any(input, bal_dict, except_for="no bal", except_return_val="0")
    if attempt:
        return attempt
    else:
        return

# Direction
def dir_set(input):
    if "across" in input:
        return "across"
    elif "l diag" in input:
        return "ldiag"
    elif "ldiag" in input:
        return "ldiag"
    elif "r diag" in input:
        return "rdiag"
    elif "rdiag" in input:
        return "rdiag"
    else:
        return

def dir_ring(input):
    if " l " in input:
        return "L"
    elif "left" in input:
        return "L"
    elif " r " in input:
        return "R"
    elif "right" in input:
        return "R"
    else:
        return

dir_parserlist = [dir_set, dir_ring]
parse_dir = one_of(dir_parserlist)

def parse_who(input):
    attempt = get_any(input, who_dict)
    if attempt:
        return attempt
    else:
        return

def parse_hand(input):
    attempt = get_any(input, hand_dict)
    if attempt:
        return attempt
    else:
        return

def parse_hands_across(input):
    attempt = get_any(input, hands_across_dict)
    if attempt:
        return attempt
    else:
        return

def parse_turn_how(input):
    attempt = get_any(input, turn_how_dict)
    if attempt:
        return attempt
    else:
        return

# looking for anything signifying additional info--if yes, return True
def extra_info_symbol(input):
    if "*" in input:
        return True
    else:
        # looking for parens NOT indicating counts--e.g."(1)"--
            # or distances--e.g. "(1x)"
        n = re.search("\((?![1-9]\))", input)
        o = re.search("\((?![1-9]x\))", input)
        if n and o:
            return True
        else:
            return False

def extra_info_text(input):
    if "next" in input:
        return True
    elif "new" in input:
        return True
    elif "slide" in input:
        return True
    elif "pull" in input:
        return True
    elif "pass thr" in input:
        return True
    elif "locate" in input:
        return True
    elif "look" in input:
        return True
    elif "prog" in input:
        return True
    elif "same" in input:
        return True
    elif "home" in input:
        return True

extra_parserlist = [extra_info_symbol, extra_info_text]
parse_extra = one_of(extra_parserlist)

# TODO ^ these are allll redundant, I should be able to do it with just 'get any'
def get_any(move_string, dict, except_for=None, except_return_val=None):
    """If given string contains any of the keys in the given dict., returns the
        corresponding value. (Unless string contains the 'except' string, in which
        case returns 'except_return_val'.)"""
    for key in dict.keys():
        if except_for:
            if except_for in move_string:
                return except_return_val
        if key in move_string:
            return dict[key]
    else:
        return

def get_extra_info(move_string, move):
    user_input = raw_input("""Does this move require additional info?
        \n(Input was: %s)
        \n1. Yes, before.
        \n2. Yes, after. (or 'y')
        \n3. Yes, before and after.
        \n4. No. (or 'n')
        \n> """ % move_string)
    while True:
        if user_input == "1":
            move.before_info = ask_for_input()
            break
        elif user_input in ["2", "y"]:
            move.moreinfo = ask_for_input()
            break
        elif user_input == "3":
            move.before_info = raw_input("Info before: ")
            move.moreinfo = raw_input("Info after: ")
            break
        elif user_input in ["4", "n"]:
            break
        else:
            print "I didn't get that, please try again."

    return move

def ask_for_input():
    return raw_input("> ")

sect_dict = {
    1 : "A1",
    2 : "A2",
    3 : "B1",
    4 : "B2"
}

movename_dict = {
    "swing" : "swing",
    "b&s" : "swing",
    "gypsy" : "gypsy",
    "dsd" : "dosido",
    "dosido" : "dosido",
    "do-si-do" : "dosido",
    "alle" : "allemande",
    "turn by" : "allemande",
    #"by the" is the hardest!
    "star" : "star",
    "circle" : "circle",
    "long lines" : "longlines",
    "f&b" : "longlines",
    "ll " : "longlines",
    "chain" : "chain",
    "down the hall" : "down_hall",
    "come back" : "come_back",
    "prom" : "promenade",
    "mad rob" : "mad_robin",
    "ca twirl" : "ca_twirl",
    "cali" :  "ca_twirl",
    "petronella" : "petronella"
    # need to cover all var's of [bal(ance)] ring [and/&] [slide/spin] R...
}

bal_dict = {
    "b&s" : True,
    "bal" : True,
}

hand_dict = {
    " l " : "L",
    "l hand" : "L",
    "left" : "L",
    "lh" : "L",
    " r " : "R",
    "r hand" : "R",
    "right" : "R",
    "rh" : "R"
}

# can't be "TO PARTNER" etc...
# maybe go thru all parsers, if find more than one then ask for clarification.
# also what about multiple things mentioned in same move line? e.g. "half hey, ladies pass R, gents ricochet over L"
who_dict = {
    "ladies" : "ladies",
    "woman" : "ladies",
    "gents" : "gents",
    "men" : "men",
    " n " : "neighbor",
    " ns " : "neighbor",
    "neighbor" : "neighbor",
    " P " : "partner",
    " ps " : "partner",
    "part" : "partner",
    "shad" : "shadow",
}

hands_across_dict = {
    "hands across" : True,
    "hands-across" : True
}

turn_how_dict = {
    "alone" : "alone",
    "couple" : "couple"
}

# http://www.cotellese.net/2007/09/27/running-external-scripts-against-django-models/
