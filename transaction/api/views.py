from transaction.api.forms import MakeTransactionForm, QueryPointsForm

from tokenapi.http import JsonResponse, JsonError

from utils.decorators import jsonp


@jsonp
def credit_points(request):
    form = MakeTransactionForm(request.POST, debit=False)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'ERROR', 'error_message': str(form.errors)})

@jsonp
def query_points(request):
    form = QueryPointsForm(request.GET)
    if form.is_valid():
        return JsonResponse({
            'status': 'OK', 'points': form.user.get_profile().points
        })
    else:
        return JsonResponse({'status': 'ERROR', 'error_message': str(form.errors)})

@jsonp
def debit_points(request):
    form = MakeTransactionForm(request.POST, debit=True)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'ERROR', 'error_message': str(form.errors)})
