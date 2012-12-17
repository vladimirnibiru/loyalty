from json import dumps

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from transaction.api.forms import MakeTransactionForm, QueryPointsForm

from logging import getLogger
log = getLogger(__name__)

@csrf_exempt
def credit_points(request):
    form = MakeTransactionForm(False, data=request.POST)
    if form.is_valid():
        form.save()
        log.info("Credit points ['OK'] POST %s" %dict(request.POST))
        return HttpResponse(dumps({'status': 'OK'}),
            mimetype='application/json')
    else:
        errors = dict(form.errors.items())
        log.info("Credit points ['ERROR'] POST %s ERRORS %s" %(dict(request.POST), errors))
        return HttpResponse(dumps({'status': 'ERROR',
            'error_message': errors}), mimetype='application/json')


def query_points(request):
    form = QueryPointsForm(request.GET)
    if form.is_valid():
        return HttpResponse(dumps({'status': 'OK', 'points': form.user.get_profile().points}),
            mimetype='application/json')
    else:
        return HttpResponse(dumps({
                'status': 'ERROR', 'error_message': dict(form.errors.items())
            }), mimetype='application/json')

@csrf_exempt
def debit_points(request):
    form = MakeTransactionForm(True, data=request.POST)
    if form.is_valid():
        form.save()
        log.info("Debit points ['OK'] POST %s" %dict(request.POST))
        return HttpResponse(dumps({'status': 'OK'}),
            mimetype='application/json')
    else:
        errors = dict(form.errors.items())
        log.info("Debit points ['ERROR'] POST %s ERRORS %s" %(dict(request.POST), errors))
        return HttpResponse(dumps({'status': 'ERROR',
            'error_message': errors}), mimetype='application/json')
