from django.shortcuts import render
from django.http import HttpResponse
from contratest.models import Dance, Move
from forms import MoveForm, DanceForm
from django.db.models import Q

def index(request):
    my_dances = Dance.objects.all()
    context = {'my_dances': my_dances, 'a_dance': my_dances[0].pretty_list()}
    return render(request, 'contratest/index.html', context)

def search(request):
    form1 = MoveForm()
    form2 = MoveForm()
    context = {'form1': form1, 'form2': form2}
    return render(request, 'contratest/search.html', context)

def results(request):

    def logic(x, argument, value):
        return getattr(x, argument) == value

    def find_first_move(search_terms):
        """Given a set of search terms (a list of (argument, value)
            pairs), returns a list of all matching moves."""
        move_query = None
        stuff = []
        for arg, val in search_terms:
            q = Q(**{"%s__exact" % arg: val})
            if move_query:
                move_query = move_query & q
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

    def match_next_moves(moves_list, search_terms):
        results = list(moves_list)
        for arg, val in search_terms:
            results = filter(lambda move: logic(move, arg, val), results)
        return results

    def find_dances(moves_list):
        """Returns a list of dances to which moves in the
            given moves_list belong (no duplicates)."""
        result_dances = []
        for move in moves_list:
            result_dances.append(move.dance)

        return list(set(result_dances))

    # make a list of all search terms as (arg, val_list) pairs
    all_search_terms = []
    for arg in Move.params:
        val_list = request.GET.getlist(arg)
        all_search_terms.append((arg, val_list))

    # TODO: this could totally be more efficient
    search_terms_by_move = []
    for i in range(0, 2):
        temp_list = []
        for pair in all_search_terms:
            try:
                if pair[1][i] != u"":
                    temp_list.append((pair[0], pair[1][i]))
            except IndexError:
                pass
        search_terms_by_move.append(temp_list)

    move1 = search_terms_by_move[0]
    move2 = search_terms_by_move[1]
    first = find_first_move(move1)
    next = find_next_moves(first)
    matched = match_next_moves(next, move2)
    dances =
    #find_dances(matched)

    '''
    dance_search_terms = []
    for arg in Dance.search_params:
        val_list = request.GET.getlist(arg)
        dance_search_terms.append((arg, val_list))

    dance_query = None
    for arg, val_list in move_search_terms:
        if val_list:
            for val in val_list:
                q = Q(**{"%s__exact" % arg: val})
                if dance_query:
                    dance_query = dance_query | q
                else:
                    dance_query = q

    # filter by dance attributes
    result_dances = result_dances.filter(dance_query)
    '''
    context = {"query": search_terms_by_move, "first": first, "next": next, "matched": matched, "dances": dances}
    return render(request, 'contratest/results.html', context)