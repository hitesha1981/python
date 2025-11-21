from django.http import JsonResponse
from .utils import fetch_prices

def prices(request):
    data = fetch_prices()
    return JsonResponse(data)
