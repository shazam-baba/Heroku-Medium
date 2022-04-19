from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.new_search, name='new_search'),
    path('results', views.results, name='results'),
    path('details/<str:pk>', views.details, name='details'),
]
