from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserForm(UserCreationForm):
    # email = forms.EmailField()

    class Meta:
        model = User

        fields = ['username', 'password1', 'password2']





class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['api_key']
        widgets = {
          'api_key': forms.Textarea(attrs={'rows':1, 'cols':1}),
        }


