from contratest.models import *

br = Dance.objects.all()[0]

testmove = Move(movename="dosido", who="ladies", dist=1.5, count=8)

mymove = Move.objects.get(pk=17)