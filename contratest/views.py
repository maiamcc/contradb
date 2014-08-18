from django.shortcuts import render
from django.http import HttpResponse
from contratest.models import Dance, Move
from forms import MoveForm
from django.db.models import Q

def index(request):
    my_dances = Dance.objects.all()
    context = {'my_dances': my_dances, 'a_dance': my_dances[0].pretty_list()}
    return render(request, 'contratest/index.html', context)

def search(request):
    form = MoveForm()
    context = {'Move': Move, 'form': form}
    return render(request, 'contratest/search.html', context)

def results(request):
    search_terms = []
    for arg in Move.params:
        val = request.GET.get(str(arg))
        search_terms.append((arg, val))

    query = None
    for arg, val in search_terms:
        if val:
            q = Q(**{"%s__exact" % arg: val})
            if query:
                query = query & q
            else:
                query = q
    result_moves = Move.objects.filter(query)
    result_dances = []
    for move in result_moves:
        result_dances.append(move.dance)
    result_dances = list(set(result_dances))
    context = {'result_moves': result_moves, 'result_dances': result_dances, 'search_terms': search_terms}
    return render(request, 'contratest/results.html', context)