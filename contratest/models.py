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
    # add notes field

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

    def pretty_print_json(self):
        return "<em>%s, by %s (%s)</em><br>" % (self.title, self.author, self.formation) \
            + "<em>A1:</em> " + "<br>".join(map(str, self.get_sect("A1"))) + "<br>" \
            + "<em>A2</em>: " + "<br>".join(map(str, self.get_sect("A2"))) + "<br>" \
            + "<em>B1</em>: " + "<br>".join(map(str, self.get_sect("B1"))) + "<br>" \
            + "<em>B2</em>: " + "<br>".join(map(str, self.get_sect("B2")))
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
            if move.movename == "swing" and move.bal == "1":
                result.append("balance and swing")
            elif move.movename == "chain":
                result.append("%s %s" % (move.who, move.movename))
            elif move.movename == "come_back":
                pass
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
        ("bal_wave", "balance the wave"),
        ("give_take", "give and take"),
        ("promenade", "promenade"),
        ("down_hall", "down the hall"),
        ("come_back", "come back"),
        ("mad_robin", "mad robin"),
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

    dir_ring_choices = (
        ("L", "left"),
        ("R", "right")
    )

    dir_set_choices = (
        ("across", "across"),
        ("ldiag", "left diagonal"),
        ("rdiag", "right diagonal"),
        ("sides", "on the sides")
    )
    # default value for chain is across... is this explicit somewhere?

    DIR_CHOICES = dir_ring_choices + dir_set_choices

    dist_whole_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6)
    )

    dist_dec_choices = (
        (.25, .25),
        (.5, .5),
        (.75, .75),
        (1, 1),
        (1.25, 1.25),
        (1.5, 1.5),
        (1.75, 1.75),
        (2, 2)
    )

    DIST_CHOICES = tuple(sorted(set(dist_whole_choices + dist_dec_choices)))

    # currently only for use in forms.
    BOOL_CHOICES = ((1, True), (0, False))

    HEY_LENGTH_CHOICES = (
        ("half", "half"),
        ("full", "full")
    )

    # WAVE_TYPE_CHOICES = (
    #     ("short", "short"),
    #     ("long", "long"),
    #     ("ladies", "ladies"),
    #     ("gents", "gents")
    #     # should ladies/gents be 'who' instead??
    # )

    BAL_DIR_CHOICES = (
        ("RL", "right, then left"),
        ("LR", "left, then right"),
        ("fwd_back", "forward and back")
    )

    bal_dir_choices_readable = {
        "RL" : "right, then left",
        "LR" : "left, then right",
        "fwd_back" : "forward and back",
        "" : ""
    }

    TURN_HOW_CHOICES = (
        ("alone", "alone"),
        ("couple", "as a couple")
    )

    PROGRESS_CHOICES = (
        ("pass_thru", "pass through"),
        ("slide_left", "slide left"),
        ("slide_right", "slide right")
    )

    progress_readable = {
        "pass_thru" : "pass through",
        "slide_left" : "slide left",
        "slide_right" : "slide right",
        "" : "" #this is hacky
    }

    dance = models.ForeignKey(Dance)
    seq = models.IntegerField(null=True) # how do i increment?
    sect = models.CharField(max_length=2, choices=SECT_CHOICES,
        null=True)
    movename = models.CharField(max_length=100, choices=MOVENAME_CHOICES)
    who = models.CharField(max_length=20, choices=WHO_CHOICES,
        default="", blank=True)
    hand = models.CharField(max_length=20, choices=HAND_CHOICES,
        default="", blank=True)
    dist = models.CharField(max_length=20, choices=DIST_CHOICES,
        default="", blank=True)
    dir = models.CharField(max_length=20, choices=DIR_CHOICES,
        default="", blank=True)
    bal = models.CharField(max_length=20, choices=BOOL_CHOICES,
        default="", blank=True)
    count = models.IntegerField(default=8, null=True)
    moreinfo = models.CharField(max_length=300, default="", blank=True)
    beginning_info = models.CharField(max_length=300, default="", blank=True)
    hands_across = models.CharField(max_length=20, choices=BOOL_CHOICES,
        default="", blank=True)
    ricochet = models.CharField(max_length=20, choices=BOOL_CHOICES,
        default="", blank=True)
    hey_length = models.CharField(max_length=50, choices=HEY_LENGTH_CHOICES,
        default="", blank=True)
    bal_dir = models.CharField(max_length=50, choices=BAL_DIR_CHOICES,
        default="", blank=True)
    # wave_type = models.CharField(max_length=50, choices=WAVE_TYPE_CHOICES,
    #     default="", blank=True)
    turn_how = models.CharField(max_length=50, choices=TURN_HOW_CHOICES,
        default="", blank=True)
    progress = models.CharField(max_length=50, choices=PROGRESS_CHOICES,
        default="", blank=True)
    params = ["dance", "seq", "sect", "movename", "who", "hand", "dist", "dir", "bal", "count", "moreinfo", "beginning_info", "hands_across", "hey_length", "ricochet", "turn_how", "progress", "bal_dir"]

    def __unicode__(self):
        if self.movename == "other":
            return self.moreinfo
        else:
            return self.print_if("beginning_info", "%s ") + \
                self.print_if("progress", "%s to " % Move.progress_readable[self.progress]) + \
                self.print_specific() + self.print_moreinfo() + self.print_count()

    def print_specific(self):
        if self.movename == "swing":
            return "%s%s swing" % (self.who, self.print_if("bal", " balance and"))
        elif self.movename == "circle":
            return "circle %s %s places" % (self.dir, self.dist)
        elif self.movename == "star":
            return "%sstar %s %s places" % (self.print_if("hands_across", "hands across "), self.hand, self.dist)
        elif self.movename == "dosido":
            return "%s do-si-do" % self.who + self.print_if("dist", " %sx")
        elif self.movename == "chain":
            return "%s chain" % self.who
        elif self.movename == "longlines":
            return "long lines"
        elif self.movename == "allemande":
            return "%s allemande %s %sx" % (self.who, self.hand, self.dist)
        elif self.movename == "seesaw":
            return "%s seesaw" % self.who + self.print_if("dist", " %sx")
        elif self.movename == "hey":
            return "%s hey, %s passing %s" % (self.hey_length, self.who, self.hand)
        elif self.movename == "gypsy":
            return "%s gypsy" % self.who + self.print_if("hand") + self.print_if("dist", " %sx")
        elif self.movename == "rlthru":
            return "R/L through" + self.print_if("dir")
        elif self.movename == "petronella":
            return "balance the ring and spin to the right"
        elif self.movename == "pass_ocean":
            return "pass the ocean"
        elif self.movename == "yearn":
            return "yearn"
        elif self.movename == "bal_wave":
            return "balance the wave" + self.print_if("bal_dir", " %s" % Move.bal_dir_choices_readable[self.bal_dir])
        elif self.movename == "give_take":
            return "give and take"
            # should this have a "who" (e.g. with neighbor), a "which side", etc?
        elif self.movename == "promenade":
            return "promenade" + self.print_if("dir")
        elif self.movename == "down_hall":
            return "down the hall"
        elif self.movename == "come_back":
            return "turn %s and come back" % self.turn_how
            # TODO: fix this print method
        elif self.movename == "mad_robin":
            return "mad robin around %s" % self.who + self.print_if("dist", " %sx")
        elif self.movename == "ca_twirl":
            return self.print_if("bal", "balance the ring and ") + "CA twirl" + self.print_if("who", " %s") + self.print_only_if("bal", "0", " (no balance!)")


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

    def print_if(self, arg, in_string=" %s", except_for=None):
        """If the given arg has a value, print it in the given string
            format (except for values given in "except_for")."""
        if getattr(self, arg) not in [None, "", except_for, False, "0"]:
            if "%s" in in_string:
                return in_string % getattr(self, arg)
            else:
                return in_string
        else:
            return ""

    def print_only_if(self, arg, value, in_string=" %s"):
        """If the given arg has the given value, print it in the given string format."""
        if getattr(self, arg) == value:
            if "%s" in in_string:
                return in_string % getattr(self, arg)
            else:
                return in_string
        else:
            return ""

# list of what values each move expects
expected_values = {
    "swing": ["who", "bal", "progress"],
    "circle": ["dir", "dist", "progress"],
    "star": ["hand", "dist", "hands_across", "progress"],
    "dosido": ["who", "dist", "progress"],
    "chain": ["who", "dir"],
    "longlines": ["progress"],
    "allemande": ["who", "hand", "dist", "progress"],
    "seesaw": ["who", "dist", "progress"],
    "hey": ["who", "hand", "hey_length", "ricochet", "progress"],
    "gypsy": ["who", "hand", "dist", "progress"],
    "rlthru": ["dir"],
    "petronella": ["progress"],
    "pass_ocean": [],
    "yearn": [],
    "bal_wave": ["bal_dir"],
    "give_take": ["progress"],
    "promenade": ["dir"],
    "down_hall": [],
    "come_back": ["turn_how"],
    "mad_robin": ["who", "dist", "progress"],
    "ca_twirl": ["who", "bal"],
    "other": ["moreinfo"]
}