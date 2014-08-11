class Dance(object):
    """Contains all of the information of a dance, including the move
    sequence and meta-data."""

    def __init__(self, title, author, formation, A1, A2, B1, B2):
        self.title = title
        self.author = author
        self.formation = formation
        # progression?
        self.A1 = A1
        self.A2 = A2
        self.B1 = B1
        self.B2 = B2

    def __repr__(self):
        output = "%s, by %s (%s)" % (self.title, self.author, self.formation)
        for move in self.moveslist:
            output = output + "\n" + str(move)

        return output

class Move(object):
    """Superclass setting all initial values for attributes
    of individual moves."""

    #TODO would be cool if these values would autocomplete
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



"""
class mymove(Move):
    def __init__(self, ... moreinfo=None):
        pass
        self.moreinfo = moreinfo

    def __str__(self):
        return ... + self.if_more_info()

    def __repr__(self):
        return "<mymove...: ... count = %s, moreinfo = %s>" \
            %
"""


