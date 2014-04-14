from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from account.models import UserProfile
from restaurant.models import Restaurant
from django.db import transaction


# Create your views here.
def custom_login(request, **kwargs):
    # redirect logged in user to home
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    else:
        return login(request, **kwargs)


@transaction.atomic
def register(request):


@login_required
@transaction.atomic
def my_restaurants(request):
    context = {}

    if request.user.userprofile.is_customer:
        context['errors'] = 'You are not registered as a restaurant owner'
        return render(request, 'account/my-restaurants.html', context)

    restaurants = Restaurant.objects.filter(owner=request.user)
    context['restaurants'] = restaurants

    return render(request, 'account/my-restaurants.html', context)


