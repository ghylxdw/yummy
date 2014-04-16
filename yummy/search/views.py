from django.shortcuts import render
from django.http import Http404, HttpResponse
from search.forms import RestaurantSearchForm
from haystack.utils.geo import Point
from django.core import serializers
from django.db import transaction
from geopy.distance import distance
import json


RESULTS_DISPLAY_NUM = 100


# Create your views here.
def search(request):
    context = {}

    if request.method != 'GET':
        raise Http404

    form = RestaurantSearchForm(request.GET)

    if not form.is_valid():
        print form.non_field_errors
        context['errors'] = 'not enough parameter passed'
        return render(request, 'search/search.html', context)

    # pass these parameter to template as hidden field for future modify-search
    context['longitude'] = form.cleaned_data['longitude']
    context['latitude'] = form.cleaned_data['latitude']
    context['q'] = form.cleaned_data['q']
    context['type'] = form.cleaned_data['type']
    context['sort_by'] = form.cleaned_data['sort_by']
    context['distance'] = form.cleaned_data['distance']
    context['address'] = form.cleaned_data['address']

    print context['longitude']
    return render(request, 'search/search.html', context)


# Create response for ajax search
@transaction.atomic
def get_search(request):

    if request.method != 'GET':
        return HttpResponse('[]', content_type="application/json")

    form = RestaurantSearchForm(request.GET)

    if not form.is_valid():
        return HttpResponse('[]', content_type="application/json")

    # get search results from search engine
    results = form.search()

    restaurant_results = []
    related_recipes = []
    center_pnt = Point(form.cleaned_data['longitude'], form.cleaned_data['latitude'])

    # order the search results based on the 'sort_by' parameter, and transform Recipe in search results to its
    # corresponding Restaurant
    if form.cleaned_data['type'] == 'r':
        if form.cleaned_data['sort_by'] == 'd':
            results = results.distance('location', center_pnt).order_by('distance')
        elif form.cleaned_data['sort_by'] == 'h':
            results = results.order_by('-avg_rating')

        if len(results) > RESULTS_DISPLAY_NUM:
            results = results[:RESULTS_DISPLAY_NUM]

        # convert object in Haystack's QuerySearchSet into Restaurant model object
        for res in results:
            restaurant_results.append(res.object)
    else:
        recipe_incl_results = []
        if form.cleaned_data['sort_by'] == 'd':
            results = results.distance('location', center_pnt).order_by('distance')

        # use set to filter out duplicate restaurant since different recipes may belong to the same restaurant
        restaurant_set = set()
        num_of_results = 0
        for res in results:
            recipe = res.object
            if recipe.restaurant_id not in restaurant_set:
                num_of_results += 1
                recipe_incl_results.append((recipe.restaurant, recipe.id, recipe.name))
                restaurant_set.add(recipe.restaurant_id)
                if num_of_results > RESULTS_DISPLAY_NUM:
                    break

        if form.cleaned_data['sort_by'] == 'h':
            recipe_incl_results.sort(key=lambda x: x[0].avg_rating, reverse=True)

        # put restaurants into restaurant_results, and put the recipe id and recipe name that is related to each
        # restaurant into related_recipes list
        for res in recipe_incl_results:
            restaurant_results.append(res[0])
            related_recipes.append((res[1], res[2]))

    # get the geo distance from searched point to each restaurants in the search results
    dis_from_ctr_point = []
    # Note! geopy use latitude first then longitude... which is the reverse order comparing to Haystack...
    center_pnt = (form.cleaned_data['latitude'], form.cleaned_data['longitude'])
    for res in restaurant_results:
        pnt = (res.location.y, res.location.x)
        dis = distance(center_pnt, pnt)
        dis_from_ctr_point.append(dis.miles)

    json_result = serializers.serialize('json', restaurant_results)

    # add the 'distance', 'recipe_id' and 'recipe_name' fields into each restaurant object in json
    unmarshall_result = json.loads(json_result)
    i = 0
    for res in unmarshall_result:
        fields = res['fields']
        fields['distance'] = dis_from_ctr_point[i]
        # leave the recipe fields as empty if the user is searching for restaurant rather than recipe
        if form.cleaned_data['type'] == 'r':
            fields['recipe_id'] = None
            fields['recipe_name'] = ''
        else:
            fields['recipe_id'] = related_recipes[i][0]
            fields['recipe_name'] = related_recipes[i][1]
        i += 1

    # serialize the modified object back to json
    json_result = json.dumps(unmarshall_result)

    print json_result
    return HttpResponse(json_result, content_type="application/json")










