from django.shortcuts import render

import os
import requests
import chainecho
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, "index.html")

@require_GET
@csrf_exempt  # Optional, depending on how you use the endpoint
def chainecho_news(request):
    try:
        api_key = os.getenv('CHAINECHO_API_KEY')  # Or settings.CHAINECHO_API_KEY
        api = chainecho.API(api_key)
        data = api.getLatestNews(limit=100)
        return JsonResponse(data, safe=False)
    except requests.exceptions.RequestException as e:
        print("Error fetching data from Chainecho:", e)
        return JsonResponse({"error": "Failed to fetch data from Chainecho"}, status=500)