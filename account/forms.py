from random import randint

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SigninForm(forms.Form):
    username = forms.CharField(max_length=30, label=_('Member Number'))
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
