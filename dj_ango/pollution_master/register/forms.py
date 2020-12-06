from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile


class UserForm(UserCreationForm):
    # email = forms.EmailField()

    class Meta:
        model = User

        fields = ['username', 'password1', 'password2']

                
        # labels = {
        #     'username': _('Username'),
        # }
        # help_texts = {
        #     'username': _(''),
        #     'password1': _('Some useful help text.'),
        #     'password2': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'username': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['api_key']
        widgets = {
          'api_key': forms.Textarea(attrs={'rows':1, 'cols':1}),
        }


