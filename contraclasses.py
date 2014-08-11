class movelist(list):
    """Adds a print method to a list for when the list contains Moves."""
    def __str__(self):
        # output = "\t" + str(self[0])
        output = str(self[0])
        for move in self[1:]:
            output += "\n" + str(move)
        return output
    # want REPR to still return <> format


class Dance(object):
    """Contains all of the information of a dance, including the move
    sequence and meta-data."""

    def __init__(self, title, author, formation, A1=None, A2=None, B1=None, B2=None):
        self.title = title
        self.author = author
        self.formation = formation
        # progression?
        self.A1 = A1
        self.A2 = A2
        self.B1 = B1
        self.B2 = B2

    def __str__(self):
        return "%s, by %s (%s)\n" % (self.title, self.author, self.formation) \
            + "A1: " + str(self.A1) + "\n" \
            + "A2: " + str(self.A2) + "\n" \
            + "B1: " + str(self.B1) + "\n" \
            + "B2: " + str(self.B2)
    def __repr__(self):
        return "<%s, %s, %s>" % (self.title, self.author, self.formation)


        return output

class Move(object):
    """Superclass setting all initial values for attributes
    of individual moves."""

    #TODO would be cool if these values would autocomplete
    #TODO set certain values to not display unless user specifies
        # e.g. if the user WANTS "ladies chain across", wants
        # count displayed, etc.
    #TODO support NEW ladies, NEXT neighbor, orig. neighbor, etc.
        # but still searchable by "neighbor" etc.
    #TODO invidid. move constructors can't deal with "count=4" etc...
    legal_values = \
        {"who": ["ladies", "gents", "partner", "neighbor", "shadow", None], \
        "hand": ["R", "L", None], \
        "dist": [1, 2, 3, 4, 5, 6, 0.25, 0.5, 0.75, 1.25, 1.5, 1.75, None], \
        "dir": ["across", "ldiag", "rdiag", "L", "R", None], \
        "count": [x for x in range(1,17)], \
        "bal": [True, False, None], \
        "hey_length": ["full", "half", None]}

    who = None
    hand = None
    dist = None
    dir = None # can I call an attribute this?
    count = 8
    moreinfo = None
    bal = None
    hey_length = None

    def __setattr__(self, attr, val):
        if self.legal_values.get(attr) and val in self.legal_values[attr]:
            object.__setattr__(self, attr, val)
        elif not self.legal_values.get(attr):
            object.__setattr__(self, attr, val)
        else:
            raise AttributeError("'%s' is not a legal value for attribute '%s'."
                % (val, attr) )

    def if_more_info(self):
        if self.moreinfo:
            return " (%s)" % self.moreinfo
        else:
            return ""

class Swing(Move):
    def __init__(self, who, bal=False, moreinfo=None):
        self.who = who
        self.bal = bal
        self.moreinfo = moreinfo
        if self.bal:
            self.count = 16

    def __str__(self):
        if self.bal:
            return "%s balance and swing" % self.who + self.if_more_info()
        else:
            return "%s swing" % self.who + self.if_more_info()

    def __repr__(self):
        return "<Swing: who = %s, bal = %s, count = %s, moreinfo = %s>" \
            % (self.who, self.bal, self.count, self.moreinfo)

class Circle(Move):
    def __init__(self, dir="L", dist=3, moreinfo=None):
        self.dir = dir
        self.dist = dist
        self.moreinfo = moreinfo

    def __str__(self):
        return "circle %s %s places" % (self.dir, self.dist) \
            + self.if_more_info()

    def __repr__(self):
        return "<Circle: dir = %s, dist = %s, count = %s, moreinfo = %s>" \
            % (self.dir, self.dist, self.count, self.moreinfo)

class Star(Move):
    def __init__(self, hand="L", dist=4, moreinfo=None):
        self.hand = hand
        self.dist = dist
        self.moreinfo = moreinfo

    def __str__(self):
        return "star %s %s places" % (self.hand, self.dist) \
            + self.if_more_info()

    def __repr__(self):
        return "<Star: hand = %s, dist = %s, count = %s, moreinfo = %s>" \
            % (self.hand, self.dist, self.count, self.moreinfo)

class Allemande(Move):
    def __init__(self, who, hand, dist, moreinfo=None):
        self.who = who
        self.hand = hand
        self.dist = dist
        self.moreinfo = moreinfo

    def __str__(self):
        return "%s allemande %s %sx" % (self.who, self.hand, self.dist) \
            + self.if_more_info()

    def __repr__(self):
        return "<Allemande: who = %s, hand = %s, dist = %s, \
            count = %s, moreinfo = %s>" % (self.who, self.hand, self.dist, \
            self.count, self.moreinfo)

class Dosido(Move):
    def __init__(self, who, dist=1, moreinfo=None):
        self.who = who
        self.dist = dist
        self.moreinfo = moreinfo

    def __str__(self):
        return "%s do-si-do %sx" % (self.who, self.dist) \
            + self.if_more_info()

    def __repr__(self):
        return "<dosido: who = %s, dist = %s, count = %s, moreinfo = %s>" \
            % (self.who, self.dist, self.count, self.moreinfo)

# TODO: order of args here unideal
class Gypsy(Move):
    def __init__(self, who, dist, hand="R", moreinfo=None):
        self.who = who
        self.hand = hand
        self.dist = dist
        self.moreinfo = moreinfo

    def __str__(self):
        return "%s gypsy by the %s %sx" % (self.who, self.hand, self.dist) \
            + self.if_more_info()

    def __repr__(self):
        return "<Gypsy: who = %s, hand = %s, dist = %s, \
            count = %s, moreinfo = %s>" % (self.who, self.hand, self.dist, \
            self.count, self.moreinfo)

class Chain(Move):
    def __init__(self, who="ladies", dir="across", moreinfo=None):
        self.who = who
        self.dir = dir
        self.moreinfo = moreinfo

    def __str__(self):
        return "%s chain" % self.who + self.if_more_info()

    def __repr__(self):
        return "<chain: who = %s, dir = %s, count = %s, moreinfo = %s>" \
            % (self.who, self.dir, self.count. self.moreinfo)

class LongLines(Move):
    def __init__(self, moreinfo=None):
        self.moreinfo = moreinfo
    def __str__(self):
        return "long lines" + self.if_more_info()

    def __repr__(self):
        return "<long lines: count = %s, moreinfo = %s>" \
            % (self.count, self.moreinfo)

# Test dances
# TODO make a better dance constructor (set sect -- give it sect.
    # to fill in and the moves, makes a movelist out of them?)


"""
class mymove(Move):
    def __init__(self, ... moreinfo=None):
        self.moreinfo = moreinfo

    def __str__(self):
        return ... + self.if_more_info()

    def __repr__(self):
        return "<mymove...: ... count = %s, moreinfo = %s>" \
            %
"""


