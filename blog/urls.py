from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('Forecasts', views.apiForecasts, name='forecasts'),
    path('ForecastsFilter', views.apiForecastsFilter, name='forecasts-filter'),
    # path('tes', views.dump_prediksi, name='tes'),
]
