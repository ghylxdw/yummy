from django import forms


class RegisterForm(forms.Form):
    email = forms.CharField(max_length=50)
    fname = forms.CharField(max_length=200, label='First Name')
    lname = forms.CharField(max_length=200, label='Last Name')
    password1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput())



