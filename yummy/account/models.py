from django.contrib.gis.db import models
# User class for built-in authentication module
from django.contrib.auth.models import User


# Create your models here.
# user profile model which is an extension of User model in django auth system
class UserProfile(models.Model):
    is_customer = models.BooleanField()
    token = models.CharField(max_length=100, db_index=True)
    user = models.OneToOneField(User, related_name="user_profile")

    def __unicode__(self):
        return self.is_customer + ' ' + self.user