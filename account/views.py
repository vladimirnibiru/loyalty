from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from account.forms import SigninForm, SignupForm
from transaction.models import Transaction

from logging import getLogger
log = getLogger(__name__)


def signin(request):
    if request.user.is_authenticated():
        return redirect('account')

    form = SigninForm(request.META['REMOTE_ADDR'], data=request.POST or None)
    if form.is_valid():
        login(request, form.user)
        log.info("User '%s' id#%s was signed-in" %(form.user.get_full_name(), form.user.id))
        return redirect('account')

    return render_to_response('account/signin.html', locals(),
        context_instance=RequestContext(request))


def signup(request):
    if request.user.is_authenticated():
        return redirect('account')

    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        log.info("User '%s' id#%s was signed-up" %(user.get_full_name(), user.id))
        return render_to_response('account/signup_success.html', locals(),
            context_instance=RequestContext(request))
    return render_to_response('account/signup.html', locals(),
        context_instance=RequestContext(request))


def account(request):
    if not request.user.is_authenticated():
        return redirect('signin')
    transactions = Transaction.objects.filter(user=request.user).order_by('-id')
    return render_to_response('account/account.html', locals(),
        context_instance=RequestContext(request))
