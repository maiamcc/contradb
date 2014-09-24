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
    def pretty_repr(d):
        for k, v in d.iteritems():
            print k
            for k1, v1 in v.iteritems():
                print "\t",k1
                for k2, v2 in v1.iteritems():
                    print "\t\t",k2,"-->",v2

    def pretty_print(d):
        results = []
        for i, v in enumerate(d.values()):
            if i != 0:
                results.append("and")
            for k1, v1 in v.iteritems():
                results.append("<pre>   %s=%s</pre>" % ("movename", v1["movename"]))
                for k2, v2 in v1.iteritems():
                    if k2 != "movename":
                        if v2:
                            val = v2
                        else:
                            val = "[any]"
                        results.append("<pre>        %s=%s</pre>" % (k2, val))


        return results

    def logic(x, argument, value):
        """Checks if x.argument == value"""
        return getattr(x, argument) == value

    def make_query(arg, val):
        return Q(**{"%s__exact" % arg: val})

    def find_first_move(search_dict):
        ### This is nice and faster than the other way of
            # doing things, but for extensibility I may have
            # to scrap it =(
        """Given a set of search terms (a list of (argument, value)
            pairs), returns a list of all matching moves."""
        move_query = None
        stuff = []
        for arg, val in search_dict.iteritems():
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
        return results

    def find_all_moves_in_dance(moves_list):
        results = []
        for move in moves_list:
            for x in Move.objects.filter(dance__exact=move.dance):
                results.append(x)
        return results

    def filter_moves_by_query(search_dict, moves_list=Move.objects.all()):
        results = list(moves_list)
        for arg, val in search_dict.iteritems():
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

    def resolve_query_dict(d, moves_list=None):
        # MUTABLE OBJS GENERALLY NOT FOR DEFAULT ARGS
        # None truth checks use 'is' not '=' b/c None is a singleton
        if moves_list is None:
            moves_list = Move.objects.all()

        first_search = d[sorted(d.keys())[0]]
        matches = filter_moves_by_query(first_search, moves_list)
        if len(d.keys()) > 1:
            for query_num, search in sorted(d.items())[1:]:
                next_moves = find_next_moves(matches)
                matches = filter_moves_by_query(search, next_moves)
        return matches

    searched_for = defaultdict(lambda : defaultdict(dict))
    for k, v in request.GET.iteritems():
        if not (k.startswith("csrf")):
            searched_for[k[-1]][int(k[-2])][k[:-2]] = v
    pretty_search_terms = pretty_print(searched_for)
    print pretty_search_terms
    moves_to_search = None
    for letter, sub_dict in searched_for.iteritems():
        moves_found = resolve_query_dict(sub_dict, moves_to_search)
        moves_to_search = find_all_moves_in_dance(moves_found)
    dances = find_dances(moves_found)

    context = {"pretty_search_terms": pretty_search_terms, "dances": dances}

    return render(request, 'contratest/results.html', context)