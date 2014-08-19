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
            results.append(Move.objects.filter(dance__exact=move.dance).filter(seq__exact=move.seq+1))
        return results

    #def match_move(search_terms, move_set):

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
                temp_list.append((pair[0], pair[1][i]))
            except IndexError:
                pass
        search_terms_by_move.append(temp_list)

    move1 = search_terms_by_move[0]
    move2 = search_terms_by_move[1]
    first = find_first_move(move1)
    # next = find_next_moves(first)
    #result_moves = find_first_move(move_search_terms)
    '''
    result_dances = []
    for move in result_moves:
        result_dances.append(move.dance)
    # list of dances containing specified move
    result_dances = list(set(result_dances))
    '''
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
    # 'result_moves': result_moves,'result_dances': result_dances,
    context = {"query": search_terms_by_move, "first": first}
    return render(request, 'contratest/results.html', context)