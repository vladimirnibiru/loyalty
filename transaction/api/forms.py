from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now

from transaction.models import Transaction


class MakeTransactionForm(forms.Form):
    account_no = forms.CharField(min_length=16, max_length=16)
    value = forms.IntegerField(min_value=0)
    activity = forms.CharField(max_length=256, required=False)
    date = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M:%S"])
    key = forms.CharField(max_length=256)

    def __init__(self, debit, data={}, *args, **kwargs):
        super(MakeTransactionForm, self).__init__(data, *args, **kwargs)
        self.debit = debit
        self.user = None

    def clean_account_no(self):
        account_no = self.cleaned_data.get('account_no', '')
        try:
            u = User.objects.get(username=account_no)
        except User.DoesNotExist:
            raise forms.ValidationError('Incorrect account_no')
        else:
            self.user = u
            return account_no

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if self.debit and self.user and self.user.get_profile().points < value:
            raise forms.ValidationError('Not enough points')
        else:
            return value

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date > now():
            raise forms.ValidationError('Date cannot be from future')
        else:
            return date

    def clean_key(self):
        key = self.cleaned_data.get('key', '')
        if key != settings.PARTNER_AUTHORIZATION_KEY:
            raise forms.ValidationError('Incorrect key')
        else:
            return key

    def save(self):
        signed_value = int(self.cleaned_data['value']) * (-1 if self.debit else 1)
        Transaction.objects.create(
            user = self.user,
            value = signed_value,
            date = self.cleaned_data['date'],
            details = self.cleaned_data.get('activity', '')
        )
        profile = self.user.get_profile()
        profile.points += signed_value
        profile.save()


class QueryPointsForm(forms.Form):
    account_no = forms.CharField(min_length=16, max_length=16)
    key = forms.CharField(max_length=256)

    def __init__(self, data={}, *args, **kwargs):
        super(QueryPointsForm, self).__init__(data, *args, **kwargs)
        self.user = None

    def clean_account_no(self):
        account_no = self.cleaned_data.get('account_no', '')
        try:
            u = User.objects.get(username=account_no)
        except User.DoesNotExist:
            raise forms.ValidationError('Incorrect account_no')
        else:
            self.user = u
            return account_no

    def clean_key(self):
        key = self.cleaned_data.get('key', '')
        if key != settings.PARTNER_AUTHORIZATION_KEY:
            raise forms.ValidationError('Incorrect key')
        else:
            return key
