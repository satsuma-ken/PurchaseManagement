from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:company_id>/', views.detail, name='detail'),
    path('<str:company_id>/results/', views.results, name='results'),
    path('<str:company_id>/vote', views.vote, name='vote'),
]