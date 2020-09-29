from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='petugas-home'),
    path('Auth', views.LoginView.as_view(), name='login'),
    path('Logout', views.logout, name='logout'),
    path('api/DataRadiasi', views.getDataRadiasi, name="apiGetDataRadiasi"),
    path('api/DataRadiasiId', views.getDataRadiasiId, name="apiGetDataRadiasiId"),
    path('InsertRadiasi', views.insertRadiasiBaru, name="insertDataRadiasi"),
    path('UpdateRadiasi', views.updateRadiasi, name="updateDataRadiasi"),
]
