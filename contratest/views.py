from django.shortcuts import render
from django.http import HttpResponse
from contratest.models import Dance, Move
from forms import MoveForm, DanceForm, testForm, individualizedForm
from django.db.models import Q
from collections import defaultdict

def index(request):
    my_dances = Dance.objects.all()
    context = {'my_dances': my_dances}
    return render(request, 'contratest/index.html', context)

def search(request):
    form = testForm()
    all_moves = Move.MOVENAME_CHOICES
    form_list = []
    for move in all_moves:
        form_list.append((move[0], individualizedForm(move[0])))
    context = {'form' : form, 'form_list' : form_list}
    return render(request, 'contratest/search.html', context)

def results(request):
    def logic(x, argument, value):
        """Checks if x.argument == value"""
        return getattr(x, argument) == value

    def make_query(arg, val):
        return Q(**{"%s__exact" % arg: val})

    def find_first_move(search_terms):
        """Given a set of search terms (a list of (argument, value)
            pairs), returns a list of all matching moves."""
        move_query = None
        stuff = []
        for arg, val in search_terms.iteritems():
            # if arg != "logic"
            if val:
                q = make_query(arg, val)
                if move_query:
                    move_query = q & move_query
                else:
                    move_query = q
        return Move.objects.filter(move_query)

    def find_next_moves(moves_list):
        results = []
        for move in moves_list:
            for x in Move.objects.filter(dance__exact=move.dance).filter(seq__exact=move.seq+1):
                results.append(x)
                # can i do this more cleanly? just appending = i appended lists rather than just the moves, and appending x for x in [[filter code]] made me generator objects. wuh?
        return results

    def filter_moves_by_query(moves_list, search_terms):
        results = list(moves_list)
        for arg, val in search_terms.iteritems():
            if val:
                results = filter(lambda move: logic(move, arg, val), results)
        return results

    def find_dances(moves_list):
        """Returns a list of dances to which moves in the
            given moves_list belong (no duplicates)."""
        result_dances = []
        for move in moves_list:
            result_dances.append(move.dance)
        return list(set(result_dances))

    print request.GET.items()
    searched_for = defaultdict(dict)
    for k, v in request.GET.iteritems():
        if not (k.startswith("csrf")):
            searched_for[int(k[-1])][k[:-1]] = v
    and_dict = filter(lambda d: d.get('logic')=="and", searched_for.values())
    follow_dict = filter(lambda d: d.get('logic')!="and", searched_for.values())
    print "Searched_for:", searched_for
    print "and_dict:", and_dict
    search_terms = searched_for[0]
    matches = find_first_move(searched_for[0])
    if len(searched_for.keys()) > 1:
        for query_num, search in sorted(searched_for.items()[1:]):
            if search["logic"] == "followed":
                next_moves = find_next_moves(matches)
                matches = filter_moves_by_query(next_moves, search)
    dances = find_dances(matches)

    #list of dicts



    context = {"searched_for": searched_for} #, "dances": dances
    return render(request, 'contratest/results.html', context)