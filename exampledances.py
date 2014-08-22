from contraclasses import *

babyrose = Dance("The Baby Rose", "David Kaynor", "improper")
babyrose.A1 = movelist([Swing("neighbor", True)])
babyrose.A2 = movelist([Circle(), Dosido("partner", 1)])
babyrose.B1 = movelist([Swing("partner", True)])
babyrose.B2 = movelist([Chain(), Star()])

ali = Dance("Ali's Safeway Produce", "Robert Cromartie", "improper")
ali.A1 = movelist([Star(), Allemande("neighbor", "L", 1.5)])
ali.A2 = movelist([Allemande("ladies", "R", 1.5), Swing("partner")])
ali.B1 = movelist([Circle(), Swing("neighbor")])
ali.B2 = movelist([LongLines(), Star("R", 1)])

reeleasy = Dance("Reel Easy", "Cary Ravitz", "improper")
reeleasy.A1 = movelist([Dosido("neighbor"), Swing("neighbor")])
reeleasy.A2 = movelist([LongLines(), Allemande("ladies", "R", 1.5)])
reeleasy.B1 = movelist([Swing("partner", True)])
reeleasy.B2 = movelist([Circle(), Allemande("neighbor", "R", 1, "and pull by")])

marycay = Dance("Mary Cay's Reel", "David Kaynor", "becket")
marycay.A1 = movelist([Circle(moreinfo="and pass thru up & down"), Allemande("neighbor", "L", 1, "a new N")])
marycay.A2 = movelist([Swing("neighbor", True, "orig. N")])
marycay.B1 = movelist([LongLines(), Allemande("ladies", "R", 0.75),\
    Allemande("ladies", "L", 0.75, "new lady")])
marycay.B2 = movelist([Swing("partner", True)])

mydances = [babyrose, ali, reeleasy, marycay]