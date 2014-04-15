from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login as login_view
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant, Review
from account.models import UserProfile
from account.forms import RegisterForm, RestaurantForm
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import Http404


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
    new_user.last_name = form.cleaned_Data['lname']
    new_user.save()

    token = default_token_generator.make_token(new_user)
    if form.cleaned_data['user_type'] == 'c':
        is_customer = True
    else:
        is_customer = False
    user_profile = UserProfile(is_customer=is_customer, token=token, user=new_user)
    user_profile.save()

    # send the activation email to the registered email address
    message = 'Click this link to activate your account: ' + 'http://localhost:8000/account/activate/' + token
    send_mail('Confirmation from blog', message, 'team39.yummy@gmail.com', [form.cleaned_data['email']], fail_silently=True)

    context['email'] = form.cleaned_data['email']
    return render(request, 'account/activate_required.html', context)


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


@login_required
@transaction.atomic
def my_reviews(request):
    if request.method != 'GET':
        raise Http404

    reviews = Review.objects.filter(reviewer=request.user).order_by("-create_time")
    context = {'reviews', reviews}
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
    context = {}
    if request.method == 'GET':
        context['form'] = RestaurantForm()
        return render(request, 'account/add-restaurant.html', context)

    form = RestaurantForm(request.POST)

    if not form.is_valid():
        context['errors'] = ''








