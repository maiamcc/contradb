class Dance(object):
    """Contains all of the information of a dance, including the move
    sequence and meta-data."""

    def __init__(self):
        pass

    def __repr__(self):
        pass

class Move(object):
    """Superclass setting all initial values for attributes
    of individual moves."""

    legal_values = {"who": ["ladies", "gents", "partner", "neighbor", "shadow", None], \
            "hand": ["R", "L", None], \
            "dist": [1, 2, 3, 4, 5, 6, 0.25, 0.5, 0.75, 1.25, 1.5, 1.75, None], \
            "dir": ["across", "ldiag", "rdiag", None], \
            "count": [x for x in range(1,17)], \
            "bal": [True, False, None], \
            "hey_length": ["full", "half", None]}

    who = None
    hand = None
    dist = None
    dir = None
    count = 8
    bal = None
    hey_length = None

    def __setattr__(self, attr, val):
        if val in self.legal_values[attr]:
            object.__setattr__(self, attr, val)
        else:
            print "No you may not", attr, val

    def __repr__(self):
        pass

class Swing(Move):
    def __init__(self, who, bal):
        self.who = who
        self.bal = bal
        if self.bal:
            self.count = 16

    def __repr__(self):
        if self.bal:
            return "%s balance and swing" % self.who
        else:
            return "%s swing" % self.who