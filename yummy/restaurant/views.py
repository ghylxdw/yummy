from django.shortcuts import render
from django.http import Http404
from restaurant.models import Restaurant, Recipe, Review
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# Create your views here.
@transaction.atomic
def restaurant_home(request, restaurant_id):
    if request.method != 'GET':
        raise Http404

    context = {}

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        restaurant = None

    if not restaurant:
        context['errors'] = 'This restaurant does not exist!'
        return render(request, 'restaurant/restaurant_homepage.html', context)

    context['restaurant'] = restaurant

    if not request.user.is_authenticated():
        context['is_login'] = False
        context['is_owner'] = False
    else:
        context['is_login'] = True
        # if the logged in user is the owner of the restaurant
        if restaurant.owner_id == request.user.id:
            context['is_owner'] = True
        else:
            context['is_owner'] = False

    reviews = Review.objects.filter(restaurant=restaurant).order_by("-create_time")
    context['reviews'] = reviews

    recipes = Recipe.objects.filter(restaurant=restaurant)
    context['recipes'] = recipes

    return render(request, 'restaurant/restaurant_homepage.html', context)


@transaction.atomic
def menu(request, restaurant_id):
    if request.method != 'GET':
        raise Http404

    context = {}

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        context['errors'] = 'This restaurant does not exist!'
        return render(request, 'restaurant/restaurant_menu.html', context)

    recipes = Recipe.objects.filter(restaurant=restaurant)
    context['recipes'] = recipes

    return render(request, 'restaurant/restaurant_menu.html', context)


@transaction.atomic
@login_required
def write_review(requst, restaurant_id):
    context = {}
    if requst.method == 'GET':
        context['restaurant_id'] = restaurant_id
        return render(requst, 'restaurant/writere_review.html', context)





