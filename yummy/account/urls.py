from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^login$', 'account.views.custom_login', {'template_name':'account/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'account.views.register', name='register'),
    url(r'^my-restaurants$', 'account.views.my_restaurants', name='my_restaurants'),
    url(r'^my-reviews$', 'account.views.my_reviews', name='my_reviews'),
    url(r'^add-restaurant$', 'account.views.add_restaurant', name='add_restaurant'),
    url(r'^edit-restaurant/(?P<restaurant_id>\d+)$', 'account.views.edit_restaurant', name='edit_restaurant'),
    url(r'^activate/(?P<token>.+)$', 'account.views.activate', name='activate'),

    # Ajax urls
    # transfer the recipe id in post data
    url(r'^upload-recipe$', 'account.views.upload_recipe', name='upload_recipe'),
    url(r'^delete-recipe$', 'account.views.delete_recipe', name='delete_recipe'),
    url(r'^cancel-add-edit-restaurant', 'account.views.cancel_add_edit_restaurant', name='cancel_add_edit_restaurant'),
)