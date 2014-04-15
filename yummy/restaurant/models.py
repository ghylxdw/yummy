from django.contrib.gis.db import models
# User class for built-in authentication module
from django.contrib.auth.models import User


# Create your models here.
# Restaurant model including geo information
class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    introduction = models.CharField(max_length=1000)
    avg_rating = models.FloatField(default=0)
    review_number = models.IntegerField(default=0)
    owner = models.ForeignKey(User)
    address = models.CharField(max_length=256)
    location = models.PointField(help_text="Represented as (longitude, latitude)")

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


# Recipe model
class Recipe(models.Model):
    name = models.CharField(max_length=256)
    picture = models.ImageField(upload_to='menu-photos', blank=True)
    restaurant = models.ForeignKey(Restaurant)

    def __unicode__(self):
        return self.name

    def get_location(self):
        return self.restaurant.location


# Review model
class Review(models.Model):
    reviewer = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    content = models.CharField(max_length=3000)
    rating = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.reviewer + ' ' + self.content + ' ' + self.restaurant


class TemporaryRecipe(models.Model):
    name = models.CharField(max_length=256)
    picture = models.ImageField(upload_to='menu-photos')

    def __unicode__(self):
        return self.name