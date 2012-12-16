from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SigninForm(forms.Form):
    username = forms.CharField(max_length=30, label=_('Member Number'),
        widget=forms.TextInput)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self):
        if self.errors:
            return self.cleaned_data
        try:
            u = User.objects.get(username=self.cleaned_data.get('username'))
        except User.DoesNotExist:
            raise forms.ValidationError('Incorrect member number')
        else:
            if not u.check_password(self.cleaned_data.get('password')):
                raise forms.ValidationError('Incorrect password')
            else:
                self.user = u
                return self.cleaned_data
