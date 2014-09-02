from contratest.models import Dance, Move
import re

def parse_dance(filename):
    text = file_to_string(filename)
    dance_list = break_input(text)
    dance = make_dance(dance_list[0])
    dance.save()
    clean_moves = clean_moves_list(dance_list[1:])
    make_all_moves(clean_moves, dance)

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

    for item in extra_indicators:
        if move_string.find(item) > -1:
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
    if attr == "who":
        if movename != "chain":
            return use_parser(input, parse_who, ask="What's the value of 'who'?")
        else:
            return use_parser(input, parse_who, default="ladies")
    elif attr == "bal":
        return use_parser(input, parse_bal, default=False)
    elif attr == "dir":
        if movename != "chain":
            return use_parser(input, parse_dir, ask="What's the value of 'dir'?")
        else:
            return use_parser(input, parse_bal, default="across")
    elif attr == "dist":
        if movename in ["circle", "star"]:
            return use_parser(input, parse_dist_whole, ask="What's the value of 'dist'? Please input in whole number of places, e.g. 'circle L 3/4' --> '3'.)")
        elif movename == "allemande":
            print "This is an alle!"
            use_parser(input, parse_dist_dec, ask="What's the value of 'dist'? Please input as a decimal.")
        elif movename in ["dosido", "gypsy", "seesaw"]:
            use_parser(input, parse_dist_dec, default=None)
    elif attr == "hand":
        return use_parser(input, parse_hand, ask="What's the value of 'hand'?")
    elif attr == "hands_across":
        return use_parser(input, parse_hands_across, default=False)
    elif attr == "turn_how":
        return use_parser(input, parse_turn_how, ask="What's the value of 'turn_how'? (Accepted values: 'alone', 'couple'.)")
    elif attr == "moreinfo":
        return raw_input("Describe this move.\n(Input was: %s)\n> " % input)

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
    if input.find("once") > -1:
        return 4
    elif input.find("half") > -1:
        return 2
    elif input.find("all the way") > -1:
        return 4
    elif input.find("1x") > -1:
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
    elif input.find("once") > -1:
        return 1
    elif input.find("1x") > -1:
        return 1
    elif input.find("half") > -1:
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
    attempt = get_any(input, bal_dict)
    if attempt:
        return attempt
    else:
        return

# Direction
def dir_set(input):
    if input.find("across") > -1:
        return "across"
    elif input.find("l diag") > -1:
        return "ldiag"
    elif input.find("ldiag") > -1:
        return "ldiag"
    elif input.find("r diag") > -1:
        return "rdiag"
    elif input.find("rdiag") > -1:
        return "rdiag"
    else:
        return

def dir_ring(input):
    if input.find(" l ") > -1:
        return "L"
    elif input.find("left") > -1:
        return "L"
    elif input.find(" r ") > -1:
        return "R"
    elif input.find("right") > -1:
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
    if input.find("*") > -1:
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
    if input.find("next") > -1:
        return True
    elif input.find("new") > -1:
        return True
    elif input.find("slide") > -1:
        return True
    elif input.find("pull") > -1:
        return True
    elif input.find("pass thr") > -1:
        return True
    elif input.find("locate") > -1:
        return True
    elif input.find("look") > -1:
        return True
    elif input.find("prog") > -1:
        return True
    elif input.find("same") > -1:
        return True
    elif input.find("home") > -1:
        return True


# TODO ^ these are allll redundant, I should be able to do it with just 'get any'
def get_any(move_string, dict):
    for key in dict.keys():
        if move_string.find(key) > -1:
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
    "down the hall": "down_hall",
    "come back": "come_back",
    "prom": "promenade"
}

bal_dict = {
    "b&s": True,
    "bal": True,
    "no bal": False
}

hand_dict = {
    " l ": "L",
    "l hand": "L",
    "left": "L",
    "lh": "L",
    " r ": "R",
    "r hand": "R",
    "right": "R",
    "rh": "R"
}

# can't be "TO PARTNER" etc...
# also what about multiple things mentioned in same move line? e.g. "half hey, ladies pass R, gents ricochet over L"
who_dict = {
    "ladies": "ladies",
    "woman": "ladies",
    "gents": "gents",
    "men": "men",
    " n ": "neighbor",
    " ns ": "neighbor",
    "neighbor": "neighbor",
    " P ": "partner",
    " ps ": "partner",
    "part": "partner",
    "shad": "shadow",
}

hands_across_dict = {
    "hands across": True,
    "hands-across": True
}

turn_how_dict = {
    "alone": "alone",
    "couple": "couple"
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
    "down_hall": [],
    "come_back": ["turn_how"],
    "other": ["moreinfo"]
}
# http://www.cotellese.net/2007/09/27/running-external-scripts-against-django-models/
