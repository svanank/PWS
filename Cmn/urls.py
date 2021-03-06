from django.urls import path, include
from Cmn import views

urlpatterns = [
    path('AdvSearchState', views.AdvSearchState, name='AdvSearchState'),
    path('AdvSearchState/<str:SearchBy>/', views.AdvSearchState, name='AdvSearchState'),
    path('AdvSearchCountry', views.AdvSearchCountry, name='AdvSearchCountry'),
    path('AdvSearchCountry/<str:SearchBy>/', views.AdvSearchCountry, name='AdvSearchCountry'),
    path('AdvSearchTerm', views.AdvSearchTerm, name='AdvSearchTerm'),
    path('AdvSearchTerm/<str:SearchBy>/', views.AdvSearchTerm, name='AdvSearchTerm'),
    path('AdvSearchCustomer', views.AdvSearchCustomer, name='AdvSearchCustomer'),
    path('AdvSearchCustomer/<str:SearchBy>/', views.AdvSearchCustomer, name='AdvSearchCustomer')
]