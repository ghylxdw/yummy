from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'home.views.home', name='home'),

    url(r'^restaurant/', include('restaurant.urls')),

    url(r'^search$', 'search.views.search', name='search'),

    url(r'^account/', include('account.urls')),

    # Ajax urls
    # transfer search parameters as get parameters
    url(r'^get-search$', 'search.views.get_search', name='get_search')
)
