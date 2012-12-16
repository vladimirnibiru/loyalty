from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from transaction.models import Transaction

class MakeTransactionForm(forms.Form):
    account_no = forms.CharField(min_length=16, max_length=16)
    value = forms.IntegerField(min_value=0)
    activity = forms.CharField(max_length=256, required=False)
    date = forms.DateTimeField(input_formats=['%s'])
    key = forms.CharField(max_length=256)

    def __init__(self, debit=False, data={}, *args, **kwargs):
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
        value = form.cleaned_data.get('value')
        if self.debit and self.user and self.user.get_profile.points < value:
            raise forms.ValidationError('Not enough points')
        else:
            return value

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date > datetime.now():
            raise forms.ValidationError('Incorrect date')
        else:
            return date

    def clean_key(self):
        key = self.cleaned_data.get('key', '')
        if key != '6ea55dad259016bfc0e117a916343c8d9ded6702':
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
        profile = user.get_profile()
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
        if key != '6ea55dad259016bfc0e117a916343c8d9ded6702':
            raise forms.ValidationError('Incorrect key')
        else:
            return key
