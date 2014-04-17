from django import forms
from django.contrib.auth.models import User
from restaurant.models import Recipe
import re


class RegisterForm(forms.Form):
    email = forms.CharField(max_length=50)
    fname = forms.CharField(max_length=200, label='First Name')
    lname = forms.CharField(max_length=200, label='Last Name')
    password1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput())
    user_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('c', 'Customer'), ('b', 'Business')])

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_email(self):
        # check the valid format of the email
        email = self.cleaned_data.get('email')
        if email and not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            raise forms.ValidationError("Invalid email format.")

        if User.objects.filter(username__exact=email):
            raise forms.ValidationError("This email is already taken.")

        return email


class RestaurantForm(forms.Form):
    name = forms.CharField(max_length=256)
    introduction = forms.CharField(max_length=1000)
    address = forms.CharField(max_length=256)
    longitude = forms.FloatField()
    latitude = forms.FloatField()
    added_recipes = forms.CharField(required=False)

    def clean_added_recipes(self):
        added_recipes = self.cleaned_data['added_recipes']
        # don't split an empty input
        if not added_recipes:
            return added_recipes

        recipe_list = added_recipes.split('_')

        for recipe_id in recipe_list:
            try:
                int(recipe_id)
            except ValueError:
                raise forms.ValidationError('some added recipe ids are not valid integer')

        return added_recipes


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['uploader']




