from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /pollution/custom
    path('custom/', views.custom, name='custom'),
]
