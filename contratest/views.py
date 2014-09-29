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
        """For debug."""
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

    def get_reqest_to_nested_dict(req):
        """Turns given GET request into a nested dict."""
        results = defaultdict(lambda : defaultdict(dict))
        for k, v in req.GET.iteritems():
            if not (k.startswith("csrf")):
                results[k[-1]][int(k[-2])][k[:-2]] = v
        return results

    def nested_dict_to_list(dict):
        """Turns a nested dict of search terms into a list of lists of dicts.
        e.g. [[A,B],[C],[D,E]] where A = {"move" : "foo", "who" : "bar"} etc.
        and [A,B] = <move defined by move query A> followed by
        <move defined by move query B>"""
        results = []
        for k, v in sorted(dict.iteritems()):
            subresults = []
            for k1, v1 in sorted(v.iteritems()):
                subresults.append(v1)
            results.append(subresults)
        return results

    # TERMINOLOGY:
    # {"move" : "swing", "who" : "partner"} = move_query (a dict. representing a collection of attributes that points to a specific move)
    # [{"move" : "foo", "who" : "bar"}, {"move" : "baz", "hand" : "R"}] = query_sequence
    # [[{"move" : "foo", "who" : "bar"}, {"move" : "baz", "hand" : "R"}], [{"move" : "swing", "who" : "partner"}]] = query_set

    def find_next_moves(moves_list):
        """Given a moves list, returns a list of moves that come directly after given moves
            in their dance."""
        results = []
        for move in moves_list:
            for x in Move.objects.filter(dance__exact=move.dance).filter(seq__exact=move.seq+1):
                results.append(x)
        return results

    def find_all_moves_in_dance(moves_list):
        """Given a moves list, returns a list of all moves belonging to the same dances as given moves."""
        results = []
        for move in moves_list:
            for x in Move.objects.filter(dance__exact=move.dance):
                results.append(x)
        return results

    def filter_moves_by_query(move_query, moves_list):
        """Returns subset of a given moves list that match search terms given in the move query."""
        results = list(moves_list)
        for attr, val in move_query.iteritems():
            if val:
                results = filter(lambda move: getattr(move, attr) == val, results)
                # results = [move for move in results if getattr(move, attr) == val]
        return results

    def resolve_query_sequence(query_seq, moves_list):
        """Resolves an ordered list of move queries (i.e. a list of dicts). Given a query
            sequence [A, B, C], where each element is a move query, returns moves
            belonging to those dances which contain moves A, B, and C in sequence."""
        if moves_list is None:
            moves_list = Move.objects.all()

        first_search = query_seq.pop(0)
        matches = filter_moves_by_query(first_search, moves_list)
        while len(query_seq) > 0:
            next_moves = find_next_moves(matches)
            matches = filter_moves_by_query(query_seq.pop(0), next_moves)
        return matches

    def resolve_query_set(query_set, moves_to_search=None):
        """Given a query set (a list of query sequences, i.e. a list of lists of move queries),
            returns moves belonging to those dances which contain fulfil all elements of the
            query set."""
        if moves_to_search is None:
            moves_to_search = Move.objects.all()

        if len(query_set) == 1:
            cur_query = query_set[0]
            answer = resolve_query_sequence(cur_query, moves_to_search)
            return answer
        else:
            cur_query = query_set[0]
            cur_results = resolve_query_sequence(cur_query, moves_to_search)
            rest_of_dances = find_all_moves_in_dance(cur_results)
            return resolve_query_set(query_set[1:], rest_of_dances)

    def find_dances(moves_list):
        """Returns a list of dances to which moves in the
            given moves_list belong (no duplicates)."""
        result_dances = []
        for move in moves_list:
            result_dances.append(move.dance)
        return list(set(result_dances))

    # make a nested dict
    searched_for = get_reqest_to_nested_dict(request)

    # send pretty formatting to page, print to console
    pretty_search_terms = pretty_print(searched_for)
    pretty_repr(searched_for)

    # make nested dict into a list
    search_term_list = nested_dict_to_list(searched_for)

    moves_found = resolve_query_set(search_term_list)
    dances = find_dances(moves_found)

    context = {"pretty_search_terms": pretty_search_terms, "dances": dances}

    return render(request, 'contratest/results.html', context)