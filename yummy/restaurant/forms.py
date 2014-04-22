from django import forms
from restaurant.models import Review
from django.utils.translation import ugettext_lazy as _


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {'rating': forms.RadioSelect()}
        labels = {'content': _('Write Review')}
        help_texts = {'content': _('Please write your reviews for this restaurant.')}

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('rating should be an int between 1 and 5')

        return rating
