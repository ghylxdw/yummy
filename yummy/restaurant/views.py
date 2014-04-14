from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from restaurant.models import Restaurant, Recipe, Review
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from restaurant.forms import ReviewForm
from django.core import serializers

from mimetypes import guess_type

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
def restaurant_menu(request, restaurant_id):
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
def write_review(request, restaurant_id):
    context = {'restaurant_id', restaurant_id}

    if request.method == 'GET':
        context['form'] = ReviewForm()
        return render(request, 'restaurant/write_review.html', context)
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        restaurant = None

    if not restaurant:
        context['errors'] = 'the belonged restaurant does not exist'
        return render(request, 'restaurant/write_review.html', context)

    review = Review(reviewer=request.user, restaurant=restaurant)
    review_form = ReviewForm(request.POST, instance=review)
    context['form'] = review_form

    if not review_form.is_valid():
        return render(request, 'restaurant/write_review.html', context)

    # save the review
    review_form.save()

    # update the average rating and number of reviews of the restaurant
    prev_avg_rating = restaurant.avg_rating
    prev_review_num = restaurant.review_number
    restaurant.avg_rating = (prev_avg_rating * prev_review_num + review_form.cleaned_data['rating']) / (prev_review_num + 1)
    restaurant.review_number += 1
    restaurant.save()

    return redirect(reverse('restaurant_home'), kwargs={'restaurant_id': restaurant_id})


# Ajax to get reviews
@transaction.atomic
def get_review(request):
    if request.method != 'GET':
        return HttpResponse('[]', content_type="application/json")

    restaurant_id_str = request.GET['restaurant_id']
    try:
        restaurant_id = int(restaurant_id_str)
    except ValueError:
        restaurant_id = None

    if not restaurant_id:
        return HttpResponse('[]', content_type="application/json")

    reviews = Review.objects.filter(restaurant_id=restaurant_id)
    ret_data = serializers.serialize('json', reviews)

    return HttpResponse(ret_data, content_type="application/json")


@transaction.atomic
def get_recipe_image(request, recipe_id):
    if request.method != 'GET':
        raise Http404

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if not recipe.picture:
        raise Http404

    content_type = guess_type(recipe.picture.name)
    return HttpResponse(recipe.picture.read(), content_type=content_type)








