from haystack import indexes
from restaurant.models import Restaurant, Recipe


class RestaurantIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    location = indexes.LocationField(model_attr='location')
    avg_rating = indexes.FloatField(model_attr='avg_rating')

    def get_model(self):
        return Restaurant


class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    location = indexes.LocationField(model_attr='get_location')

    def get_model(self):
        return Recipe