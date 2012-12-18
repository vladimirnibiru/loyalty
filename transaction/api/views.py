from json import loads, dumps

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from transaction.api.forms import MakeTransactionForm, QueryPointsForm

from logging import getLogger
log = getLogger(__name__)

@csrf_exempt
def credit_points(request):
    if request.method != 'POST':
        return HttpResponse(dumps({
                'status': 'ERROR', 'error_message': 'POST-request only'
            }), mimetype='application/json')
    data = loads(request.body)
    form = MakeTransactionForm(False, data=data)
    if form.is_valid():
        form.save()
        log.info("Credit points ['OK'] POST %s" %data)
        return HttpResponse(dumps({'status': 'OK'}),
            mimetype='application/json')
    else:
        errors = str(dict(form.errors.items()))
        log.info("Credit points ['ERROR'] POST %s ERRORS %s" %(data, errors))
        return HttpResponse(dumps({'status': 'ERROR',
            'error_message': errors}), mimetype='application/json')


def query_points(request):
    if request.method != 'GET':
        return HttpResponse(dumps({
                'status': 'ERROR', 'error_message': 'GET-request only'
            }), mimetype='application/json')
    data = loads(request.body)
    form = QueryPointsForm(data)
    if form.is_valid():
        return HttpResponse(dumps({'status': 'OK', 'points': form.user.get_profile().points}),
            mimetype='application/json')
    else:
        return HttpResponse(dumps({
                'status': 'ERROR', 'error_message': str(dict(form.errors.items()))
            }), mimetype='application/json')

@csrf_exempt
def debit_points(request):
    if request.method != 'POST':
        return HttpResponse(dumps({
                'status': 'ERROR', 'error_message': 'POST-request only'
            }), mimetype='application/json')
    data = loads(request.body)
    form = MakeTransactionForm(True, data=data)
    if form.is_valid():
        form.save()
        log.info("Debit points ['OK'] POST %s" %data)
        return HttpResponse(dumps({'status': 'OK'}),
            mimetype='application/json')
    else:
        errors = str(dict(form.errors.items()))
        log.info("Debit points ['ERROR'] POST %s ERRORS %s" %(data, errors))
        return HttpResponse(dumps({'status': 'ERROR',
            'error_message': errors}), mimetype='application/json')
