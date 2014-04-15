from haystack.forms import SearchForm
from django import forms
from restaurant.models import Restaurant, Recipe
from haystack.utils.geo import Point, D


class RestaurantSearchForm(SearchForm):
    sort_by = forms.CharField()
    distance = forms.IntegerField()
    type = forms.CharField()
    longitude = forms.FloatField()
    latitude = forms.FloatField()
    address = forms.CharField()

    def clean_sort_by(self):
        sort_by = self.cleaned_data['sort_by']

        if sort_by != 'b' and sort_by != 'h' and sort_by != 'd':
            raise forms.ValidationError('sort_by parameter should be b or h or d')

        return sort_by

    def clean_type(self):
        type = self.cleaned_data['type']

        if type != 'r' and type != 'm':
            raise forms.ValidationError('type parameter should be r or m')

        return type

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        sqs = self.searchqueryset

        if self.cleaned_data['type'] == 'r':
            sqs = sqs.models(Restaurant)
        else:
            sqs = sqs.models(Recipe)

        if self.load_all:
            sqs = sqs.load_all()

        center_pnt = Point(self.cleaned_data['longitude'], self.cleaned_data['latitude'])
        distance_from_pnt = D(mi=int(self.cleaned_data['distance']))

        # if the query is empty, just search based on location
        if not 'q' in self.cleaned_data or not self.cleaned_data['q']:
            sqs = sqs.dwithin('location', center_pnt, distance_from_pnt)
        else:
            sqs = sqs.auto_query(self.cleaned_data['q']).dwithin('location', center_pnt, distance_from_pnt)

        # sqs = super(RestaurantSearchForm, self).search()

        return sqs

