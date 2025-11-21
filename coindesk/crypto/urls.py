from django.urls import path
from .views import prices

urlpatterns = [
    path("prices/", prices, name="crypto-prices"),
]