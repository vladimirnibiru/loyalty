from random import randint

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from lockout.exceptions import LockedOut

from logging import getLogger
log = getLogger(__name__)


class SigninForm(forms.Form):
    username = forms.CharField(max_length=30, label=_('Member Number'))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def __init__(self, IP, data={}, *args, **kwargs):
        super(SigninForm, self).__init__(data, *args, **kwargs)
        self.IP = IP

    def clean(self):
        if self.errors:
            return self.cleaned_data
        try:
            user = authenticate(username=self.cleaned_data['username'],
                password=self.cleaned_data['password'])
        except LockedOut:
            log.warn("Username '%s' was locked out (IP: %s)" %(self.cleaned_data['username'], self.IP))
            raise forms.ValidationError('You are locked out')
        else:
            if user:
                self.user = user
                return self.cleaned_data
            else:
                raise forms.ValidationError('Authentication failed')


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput,
        }

    email = forms.EmailField()
    confirm_password = forms.CharField(max_length=128,
        widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.errors:
            return email
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError('This email already used')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password', '')
        confirm_password = self.cleaned_data.get('confirm_password')
        if self.errors:
            return confirm_password
        if password != confirm_password:
            raise forms.ValidationError('Passwords doesn\'t match')
        return confirm_password

    def save(self, commit=True):
        instance = super(SignupForm, self).save(commit=False)
        instance.set_password(self.cleaned_data.get('password'))
        while True:
            instance.username = ''.join([str(randint(0, 9))\
                for i in range(0, 16)])
            try:
                User.objects.get(username=instance.username)
            except User.DoesNotExist:
                break
        if commit:
            instance.save()
        return instance
