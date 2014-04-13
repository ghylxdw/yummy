from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^(?P<restaurant_id>\d+)$', 'restaurant.views.restaurant_home', name='restaurant'),
    url(r'^write-review/(?P<restaurant_id>\d+)$', 'restaurant.views.write_review', name='write_review'),
    url(r'^menu/(?P<restaurant_id>\d+)$', 'restaurant.views.menu', name='menu'),

    # Ajax urls
    # transfer restaurant id in get parameter
    url(r'^get-reviews$', 'restaurant.views.get_reviews', name='get_reviews'),
)