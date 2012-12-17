from json import dumps

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from transaction.api.forms import MakeTransactionForm, QueryPointsForm

@csrf_exempt
def credit_points(request):
    form = MakeTransactionForm(False, data=request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse(dumps({'status': 'OK'}),
            mimetype='application/json')
    else:
        return HttpResponse(dumps({
                'status': 'ERROR', 'error_message': dict(form.errors.items())
            }), mimetype='application/json')


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
        return HttpResponse(dumps({'status': 'OK'}),
            mimetype='application/json')
    else:
        return HttpResponse(dumps({
                'status': 'ERROR', 'error_message': dict(form.errors.items())
            }), mimetype='application/json')
