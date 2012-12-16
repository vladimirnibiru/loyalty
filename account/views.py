from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from account.forms import SigninForm, SignupForm


def signin(request):
    if request.user.is_authenticated():
        return redirect('account')

    form = SigninForm(request.POST or None)
    if form.is_valid():
        login(request, form.user)
        return redirect('account')

    return render_to_response('account/signin.html', locals(),
        context_instance=RequestContext(request))


def signup(request):
    if request.user.is_authenticated():
        return redirect('account')

    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        return render_to_response('account/signup_success.html', locals(),
            context_instance=RequestContext(request))
    return render_to_response('account/signup.html', locals(),
        context_instance=RequestContext(request))


def account(request):
    if not request.user.is_authenticated():
        return redirect('signin')
    return render_to_response('account/account.html', locals(),
        context_instance=RequestContext(request))
