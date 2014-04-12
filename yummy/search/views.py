from django.shortcuts import render
from django.http import Http404
from search.forms import SearchForm
from haystack.utils.geo import Point


RESULTS_DISPLAY_NUM = 100


# Create your views here.
def search(request):
    context = {}

    if request.method == 'POST':
        raise Http404

    form = SearchForm(request.GET)

    if not form.is_valid():
        context['search_results'] = []
        return render(request, 'search/search.html')

    results = form.search()

    if form.cleaned_data['type'] == 'r':
        if form.cleaned_data['sort_by'] == 'd':
            center_pnt = Point(form.cleaned_data['longitude'], form.cleaned_data['latitude'])
            results = results.distance('location', center_pnt).order_by('distance')
        elif form.cleaned_data['sort_by'] == 'h':
            results = results.order_by('-avg_rating')

        if len(results) > RESULTS_DISPLAY_NUM:
            results = results[:RESULTS_DISPLAY_NUM]

        search_results = []
        for restaurant in results:
            search_results.append(restaurant)
        context['search_results'] = search_results

        return render(request, 'search/search.html', context)
    else:
        if form.cleaned_data['sort_by'] == 'd':
            center_pnt = Point(form.cleaned_data['longitude'], form.cleaned_data['latitude'])
            results = results.distance('location', center_pnt).order_by('distance')

        restaurant_set = {}
        search_results = []
        num_of_results = 0
        for recipe in results:
            if recipe.restaurant_id not in restaurant_set:
                num_of_results += 1
                search_results.append(recipe.restaurant)
                set.add(recipe.restaurant_id)
                if num_of_results > RESULTS_DISPLAY_NUM:
                    break

        if form.cleaned_data['sort_by'] == 'h':
            search_results.sort(key=lambda x: x.avg_rating, reverse=True)

        context['search_results'] = search_results
        return render(request, 'search/search.html', context)


    # center_pnt = fromstr("POINT(%s %s") % (form.cleaned_data['longitude'], form.cleaned_data['latitude'])
    # distance_from_point = {'mi':form.cleaned_data['distance']}
    #
    # close_restaurants_sorted = Restaurant.objects.filter(location__distance_lte=(center_pnt, D(**distance_from_point)))\
    #     .distance(center_pnt).order_by('distance')
    #
    #
    # if len(close_restaurants_sorted) > 100:
    #     close_restaurants_sorted = close_restaurants_sorted[:100]







