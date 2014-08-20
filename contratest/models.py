from django.db import models

class Dance(models.Model):
    FORMATION_CHOICES = (
        ("imp", "improper"),
        ("becketcw", "becket CW"),
        ("becketccw", "becket CCW"),
    )

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    formation = models.CharField(max_length=200, default="improper")
    progression = models.IntegerField(default=1)
    tags = models.CharField(max_length=200, blank=True)
    begins = models.CharField(max_length=200, null=True, blank=True)

    search_params = ["formation", "progression"]

    def __unicode__(self):
        return "%s by %s (%s, %ix prog.)" % (self.title, self.author, self.formation, self.progression)

    def pretty_print(self):
        """Prints a nicely formatted string rep. of the dance."""
        return "%s, by %s (%s)\n" % (self.title, self.author, self.formation) \
            + "A1: " + "\n".join(map(str, self.get_sect("A1"))) + "\n" \
            + "A2: " + "\n".join(map(str, self.get_sect("A2"))) + "\n" \
            + "B1: " + "\n".join(map(str, self.get_sect("B1"))) + "\n" \
            + "B2: " + "\n".join(map(str, self.get_sect("B2")))

    def pretty_list(self):
        """Returns a nicely formatted line-by-line rep. of the dance,
            in a list."""
        return self.pretty_print().split("\n")

    def get_sect(self, sect):
        """Returns a list of moves of the given sect. of the dance (e.g. "B1")."""
        return self.move_set.filter(sect=sect)

    def moves_list(self):
        result = []
        for move in self.move_set.all():
            if move.movename == "swing" and move.bal:
                result.append("balance and swing")
            elif move.movename == "chain":
                result.append("%s %s" % (move.who, move.movename))
            else:
                result.append(move.movename)
        return list(set(result))

    def moves_string(self):
        return ", ".join(self.moves_list())

class Move(models.Model):

    SECT_CHOICES = (
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
    )

    MOVENAME_CHOICES = (
        ("swing", "swing"),
        ("circle", "circle"),
        ("star", "star"),
        ("dosido", "do-si-do"),
        ("chain", "chain"),
        ("longlines", "long lines"),
        ("allemande", "allemande"),
        ("seesaw", "seesaw"),
        ("hey", "hey"),
        ("gypsy", "gypsy"),
        ("rlthru", "R/L through"),
        ("petronella", "petronella"),
        ("pass_ocean", "pass the ocean"),
        ("yearn", "yearn"),
        ("wave", "wave"),
        ("give_take", "give_and_take"),
        ("other", "other")
    )

    WHO_CHOICES = (
        ("ladies", "ladies"),
        ("gents", "gents"),
        ("partner", "partner"),
        ("neighbor", "neighbor"),
        ("shadow", "shadow")
    )

    HAND_CHOICES = (
        ("L", "left"),
        ("R", "right"),
    )

    DIR_CHOICES = (
        ("L", "left"),
        ("R", "right"),
        ("across", "across"),
        ("ldiag", "left diagonal"),
        ("rdiag", "right diagonal")
    )

    HEY_LENGTH_CHOICES = (
        ("half", "half"),
        ("full", "full")
    )

    WAVE_LENGTH_CHOICES = (
        ("short", "short"),
        ("long", "long")
    )

    dance = models.ForeignKey(Dance)
    seq = models.IntegerField(null=True) # how do i increment?
    sect = models.CharField(max_length=2, choices=SECT_CHOICES,
        null=True)
    movename = models.CharField(max_length=100, choices=MOVENAME_CHOICES)
    who = models.CharField(max_length=20, choices=WHO_CHOICES,
        default="", blank=True)
    hand = models.CharField(max_length=20, choices=HAND_CHOICES,
        default="", blank=True)
    dist = models.DecimalField(max_digits=3, decimal_places=2,
        null=True, blank=True)
    dir = models.CharField(max_length=20, choices=DIR_CHOICES,
        default="", blank=True)
    bal = models.NullBooleanField(null=True)
    count = models.IntegerField(default=8, null=True)
    moreinfo = models.CharField(max_length=300, default="", blank=True)
    hands_across = models.NullBooleanField(blank=True)
    rollaway = models.NullBooleanField(blank=True)
    ricochet = models.NullBooleanField(blank=True)
    hey_length = models.CharField(max_length=50, choices=HEY_LENGTH_CHOICES,
        default="", blank=True)
    hey_length = models.CharField(max_length=50, choices=WAVE_LENGTH_CHOICES,
        default="", blank=True)

    params = ["dance", "seq", "sect", "movename", "who", "hand", "dist", "dir", "bal", "count", "moreinfo", "hands_across", "hey_length", "ricochet", "rollaway"]

    def __unicode__(self):
        return self.print_specific() + self.print_moreinfo() + self.print_count()

    def print_specific(self):
        if self.movename == "swing":
            return "%s%s swing" % (self.who, self.print_if("bal", " balance and"))
        elif self.movename == "circle":
            return "circle %s %s places" % (self.dir, self.dist)
        elif self.movename == "star":
            return "%sstar %s %d places" % (self.print_if("hands_across", "hands across "), self.hand, self.dist)
        elif self.movename == "dosido":
            return "%s do-si-do" % self.who + self.print_if("dist", "%sx")
        elif self.movename == "chain":
            return "%s chain" % self.who
        elif self.movename == "longlines":
            return "long lines" + self.print_if("rollaway", " with a rollaway")
        elif self.movename == "allemande":
            return "%s allemande %s %sx" % (self.who, self.hand, self.dist)

    #can be combined into print_if...?
    def print_moreinfo(self):
        if self.moreinfo:
            return " (%s)" % self.moreinfo
        else:
            return ""

    def print_count(self):
        """For adding the number of counts, formatted, to a move string"""
        # eventually should have option for printing all vs. printing only weird
        return " (%d)" % self.count

    def print_if(self, arg, in_string="%s", except_for=None):
        """If the given arg has a value, print it in the given string
            format (except for values given in "except_for")."""
        if getattr(self, arg) not in [None, "", except_for, False]:
            if in_string.find("%s") > -1:
                return in_string % getattr(self, arg)
            else:
                return in_string
        else:
            return ""