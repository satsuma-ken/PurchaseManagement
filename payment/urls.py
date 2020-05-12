from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:company_id>/', views.detail, name='detail'),
    path('<str:company_id>/results/', views.results, name='results'),
    path('<str:company_id>/vote', views.vote, name='vote'),
    path('bills/', views.bills, name='bills'),
]