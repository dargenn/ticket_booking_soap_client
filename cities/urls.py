from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('buy_ticket', views.buy_ticket, name='buy_ticket'),
    path('confirm_ticket', views.confirm_ticket, name='confirm_ticket'),
    path('find_ticket', views.find_ticket, name='find_ticket'),
    path('find_ticket_confirmation', views.find_ticket_confirmation, name='find_ticket_confirmation')
]