from django.shortcuts import render
from django.http import Http404, HttpResponse
from search.forms import RestaurantSearchForm
from haystack.utils.geo import Point
from django.core import serializers
from django.db import transaction


RESULTS_DISPLAY_NUM = 100


# Create your views here.
def search(request):
    context = {}

    if request.method != 'GET':
        raise Http404

    form = RestaurantSearchForm(request.GET)

    if not form.is_valid():
        context['errors'] = 'not enough parameter passed'
        return render(request, 'search/search.html', context)

    # pass these parameter to template as hidden field for future modify-search
    context['longitude'] = form.cleaned_data['longitude']
    context['latitude'] = form.cleaned_data['latitude']
    context['q'] = form.cleaned_data['q']
    context['type'] = form.cleaned_data['type']
    context['sort_by'] = form.cleaned_data['sort_by']
    context['distance'] = form.cleaned_data['distance']

    return render(request, 'search/search.html', context)


# Create response for ajax search
@transaction.atomic
def get_search(request):

    if request.method != 'GET':
        return HttpResponse('[]', content_type="application/json")

    form = RestaurantSearchForm(request.GET)

    if not form.is_valid():
        return HttpResponse('[]', content_type="application/json")

    results = form.search()
    search_results = []

    if form.cleaned_data['type'] == 'r':
        if form.cleaned_data['sort_by'] == 'd':
            center_pnt = Point(form.cleaned_data['longitude'], form.cleaned_data['latitude'])
            results = results.distance('location', center_pnt).order_by('distance')
        elif form.cleaned_data['sort_by'] == 'h':
            results = results.order_by('-avg_rating')

        if len(results) > RESULTS_DISPLAY_NUM:
            results = results[:RESULTS_DISPLAY_NUM]

        for res in results:
            search_results.append(res.object)

    else:
        if form.cleaned_data['sort_by'] == 'd':
            center_pnt = Point(form.cleaned_data['longitude'], form.cleaned_data['latitude'])
            results = results.distance('location', center_pnt).order_by('distance')

        restaurant_set = {}
        num_of_results = 0
        for res in results:
            recipe = res.object
            if recipe.restaurant_id not in restaurant_set:
                num_of_results += 1
                search_results.append(recipe.restaurant)
                set.add(recipe.restaurant_id)
                if num_of_results > RESULTS_DISPLAY_NUM:
                    break

        if form.cleaned_data['sort_by'] == 'h':
            search_results.sort(key=lambda x: x.avg_rating, reverse=True)

    ret_data = serializers.serialize('json', search_results)
    return HttpResponse(ret_data, content_type="application/json")










