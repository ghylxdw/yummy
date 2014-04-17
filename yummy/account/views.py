from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login as login_view
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant, Review, Recipe
from account.models import UserProfile
from account.forms import RegisterForm, RestaurantForm, RecipeForm
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from haystack.utils.geo import Point
import json
import threading


# Create your views here.
def custom_login(request, **kwargs):
    # redirect logged in user to home
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    else:
        return login_view(request, **kwargs)


@transaction.atomic
def register(request):
    if request.user.is_authenticated():
        redirect(reverse('home'))

    context = {}
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'account/register.html', context)

    form = RegisterForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'account/register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
    new_user.is_active = False
    new_user.first_name = form.cleaned_data['fname']
    new_user.last_name = form.cleaned_data['lname']
    new_user.save()

    token = default_token_generator.make_token(new_user)
    if form.cleaned_data['user_type'] == 'c':
        is_customer = True
    else:
        is_customer = False
    user_profile = UserProfile(is_customer=is_customer, token=token, user=new_user)
    try:
        user_profile.save()
    except IntegrityError:
        context['errors'] = 'another user has already used this email address'
        return render(request, 'account/register.html', context)

    subject = 'Confirmation from Yummy'
    message = 'Click this link to activate your account: ' + 'http://ghylxdw.homeip.net:8000/account/activate/' + token
    from_addr = 'team39.yummy@gmail.com'
    recipients = [form.cleaned_data['email']]
    # send the activation email to the registered email address asynchronously by starting a daemon thread
    t = threading.Thread(target=send_mail, args=[subject, message, from_addr, recipients], kwargs={'fail_silently': True})
    t.setDaemon(True)
    t.start()

    context['email'] = form.cleaned_data['email']
    return render(request, 'account/activate-required.html', context)


@login_required
@transaction.atomic
def my_restaurants(request):
    context = {'user': request.user}

    if request.user.userprofile.is_customer:
        context['errors'] = 'You are not registered as a restaurant owner'
        return render(request, 'account/my-restaurants.html', context)

    restaurants = Restaurant.objects.filter(owner=request.user)
    context['restaurants'] = restaurants

    return render(request, 'account/my-restaurants.html', context)


@login_required
@transaction.atomic
def my_reviews(request):
    if request.method != 'GET':
        raise Http404

    context = {'user': request.user}
    reviews = Review.objects.filter(reviewer=request.user).order_by("-create_time")
    context['reviews'] = reviews
    return render(request, 'account/my-reviews.html', context)


@transaction.atomic
def activate(request, token):
    if request.method != 'GET':
        raise Http404

    if request.user.is_authenticated():
        return redirect(reverse('home'))

    context = {}
    try:
        user_profile = UserProfile.objects.get(token=token)
    except UserProfile.DoesNotExist:
        user_profile = None

    if not user_profile:
        context['errors'] = 'token invalid'
        return render(request, 'account/activate-page.html', context)

    user = user_profile.user
    user.is_active = True

    # a tricky method to log a user in without password given
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return render(request, 'account/activate-page.html', context)


@login_required
@transaction.atomic
def add_restaurant(request):
    context = {'user': request.user}
    if request.user.userprofile.is_customer:
        context['errors'] = 'you are not a business user and cannot create a restaurant'
        return render(request, 'account/add-restaurant.html', context)

    if request.method == 'GET':
        context['form'] = RestaurantForm()
        return render(request, 'account/add-restaurant.html', context)

    form = RestaurantForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'account/add-restaurant.html', context)

    location = Point(form.cleaned_data['longitude'], form.cleaned_data['latitude'])
    new_restaurant = Restaurant(name=form.cleaned_data['name'], introduction=form.cleaned_data['introduction'],
                                address=form.cleaned_data['address'], owner=request.user, location=location)
    new_restaurant.save()
    added_recipes = form.cleaned_data['added_recipes']
    relate_added_recipes_helper(new_restaurant, added_recipes)

    return redirect(reverse('restaurant_home'), kwargs={'restaurant_id': new_restaurant.id})


@login_required
@transaction.atomic
def edit_restaurant(request, restaurant_id):
    context = {'user': request.user}
    if request.user.userprofile.is_customer:
        context['errors'] = 'you are not a business user and cannot create a restaurant'
        return render(request, 'account/add-restaurant.html', context)

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        context['errors'] = 'restaurant id invalid'
        return render(request, 'account/edit-restaurant.html', context)

    if restaurant.owner != request.user:
        context['errors'] = 'you have no access to edit this restaurant'
        return render(request, 'account/edit-restaurant.html', context)

    if request.method == 'GET':
        # since we are not using a model form, we have to render and bound the existing data to the form manually
        rest_dict = {'name': restaurant.name, 'introduction': restaurant.introduction, 'address': restaurant.address,
                     'longitude': restaurant.location.x, 'latitude': restaurant.location.y}
        form = RestaurantForm(rest_dict)
        context['form'] = form

        # get all recipes that belong to the restaurant
        recipes = Recipe.objects.filter(restaurant=restaurant)
        context['recipes'] = recipes

        return render(request, 'account/edit-restaurant.html', context)
    else:
        form = RestaurantForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            return render(request, 'account/edit-restaurant.html', context)

        added_recipes = form.cleaned_data['added_recipes']
        relate_added_recipes_helper(restaurant, added_recipes)

        return redirect(reverse('restaurant_home'), kwargs={'restaurant_id': restaurant.id})


@transaction.atomic
def relate_added_recipes_helper(restaurant, added_recipes):
    for recipe_str in added_recipes.split('_'):
        recipe_id = int(recipe_str)
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.restaurant = restaurant
            recipe.save()
        except Recipe.DoesNotExist:
            pass


## Ajax view below ##
@transaction.atomic
def upload_recipe(request):
    if not request.user.is_authenticated() or request.user.userprofile.is_customer or request.method == 'GET':
        raise Http404

    new_recipe = Recipe(uploader=request.user)
    form = RecipeForm(request.POST, request.FILES, instance=new_recipe)
    if not form.is_valid():
        raise Http404

    new_recipe = form.save()

    marshalled_data = {'id': new_recipe.id, 'name': new_recipe.name}
    json_data = json.dumps(marshalled_data)

    return HttpResponse(json_data, content_type="application/json")


@transaction.atomic
def delete_recipe(request):
    if not request.user.is_authenticated() or request.user.userprofile.is_customer or request.method == 'GET':
        raise Http404

    if not 'id' in request.POST or not request.POST['id']:
        raise Http404

    try:
        recipe_id = int(request.POST['id'])
    except ValueError:
        raise Http404

    try:
        drop_recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404

    if drop_recipe.uploader != request.user:
        raise Http404

    drop_recipe.delete()

    return HttpResponse()


@transaction.atomic
def cancel_add_edit_restaurant(request):
    if not request.user.is_authenticated() or request.user.userprofile.is_customer or request.method == 'GET':
        raise Http404

    if not 'delete_recipes' in request.POST or not request.POST['delete_recipes']:
        raise Http404

    recipe_id_list = request.POST['delete_recipes'].split('_')

    for recipe_id_str in recipe_id_list:
        try:
            recipe_id = int(recipe_id_str)
            recipe = Recipe.objects.get(id=recipe_id)
            # delete the recipe only if the recipe is temporary added ('restaurant' field is null) and the recipe is
            # uploaded by the current user
            if not recipe.restaurant and recipe.uploader == request.user:
                recipe.delete()
        except ValueError, Recipe.DoesNotExist:
            pass

    return HttpResponse()