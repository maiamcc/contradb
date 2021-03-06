from django.shortcuts import render
from django.http import HttpResponse
from contratest.models import Dance, Move
from forms import MoveForm, SectForm, IndividualizedForm
from django.db.models import Q
from collections import defaultdict

def index(request):
    my_dances = Dance.objects.all()
    context = {'my_dances': my_dances}
    return render(request, 'contratest/index.html', context)

def search(request):
    move_form = MoveForm()
    sect_form = SectForm()
    all_moves = Move.MOVENAME_CHOICES
    form_list = [(move[0], IndividualizedForm(move[0])) for move in all_moves]

    context = {'move_form' : move_form, 'sect_form' : sect_form, 'form_list' : form_list}
    return render(request, 'contratest/search.html', context)

def results(request):

    # TERMINOLOGY:
        # {"move" : "swing", "who" : "partner"} = move query -- a dict. representing a
            # collection of attributes that points to a specific move
        # [{"move" : "foo", "who" : "bar"}, {"move" : "baz", "hand" : "R"}] = query sequence --
            # one or more move queries to be searched for in sequence (e.g. move A followed
            # by move B)
        # [[{"move" : "foo", "who" : "bar"}, {"move" : "baz", "hand" : "R"}],
            # [{"move" : "swing", "who" : "partner"}]] = query set -- multiple query sequences
            # and'ed together (e.g. <move A followed by move B> AND <move C>)
    def make_nested_list(req):
        letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

        sorted_search_terms = sorted(req.GET.items(), key=lambda kv: kv[0][-2])
        last_num = None
        last_let = None
        results = []
        for attr, val in sorted_search_terms:
            if attr.startswith("csrf"):
                pass
            elif attr.startswith("sect"):
                letter_index = letters.index(attr[-1])
                for move_query in results[letter_index]:
                    if val in ["A","B"]:
                        move_query["sect"] = [val+"1", val+"2"]
                    else:
                        move_query["sect"] = [val]
            else:
                cur_num = attr[-2]
                cur_let = attr[-1]
                if cur_let != last_let:
                    results.append([])
                if cur_num != last_num:
                    results[-1].append({attr[:-2] : [val]})
                else:
                    results[-1][-1][attr[:-2]] = [val]

                last_num = cur_num
                last_let = cur_let
        # [[A,B], [C], [D,E]]
        return results

    def pretty_print(search_list):
        results = []
        for i, query_seq in enumerate(search_list):
            if i != 0:
                results.append("and")

            for move_query in query_seq:
                results.append("<pre>   %s=%s</pre>" % ("movename", move_query["movename"]))
                for attr, val in sorted(move_query.iteritems()):
                    if attr != "movename":
                        if val:
                            val_text = val
                        else:
                            val_text = "[any]"
                        results.append("<pre>        %s=%s</pre>" % (attr, val_text))
        return results

    def is_wildcard(x):
        """Checks if given value is a wildcard (currently, [""])."""
        if x == [""]:
            return True
        else:
            return False

    def find_next_moves(moves_list):
        """Given a moves list, returns a list of moves that come directly after given moves
            in their dance."""
        results = []
        for move in moves_list:
            results.extend(Move.objects.filter(dance__exact=move.dance).filter(seq__exact=move.seq+1))
        return results

    def find_all_moves_in_dance(moves_list):
        """Given a moves list, returns a list of all moves belonging to the same dances as given moves."""
        results = []
        for move in moves_list:
            results.extend(Move.objects.filter(dance__exact=move.dance))
        return results

    def filter_moves_by_query(move_query, moves_list):
        """Returns subset of a given moves list that match search terms given in the move query."""
        results = list(moves_list)
        for attr, val in move_query.iteritems():
            if not is_wildcard(val):
                results = filter(lambda move: getattr(move, attr) in val, results)
        return results

        # return [move for move in moves_list
        #     if all(getattr(move, key) == val
        #            for key, val in move_query.items() if val)]

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
        return list(set([move.dance for move in moves_list]))

    for thing in sorted(request.GET.items(), key=lambda kv: kv[0][-2]):
        print thing

    # make nested list from GET request, format prettily for screen
    search_term_list = make_nested_list(request)
    pretty_search_terms = pretty_print(search_term_list)

    # find dances that meet search criteria
    moves_found = resolve_query_set(search_term_list)
    dances = find_dances(moves_found)

    context = {"pretty_search_terms": pretty_search_terms, "dances": dances}

    return render(request, 'contratest/results.html', context)