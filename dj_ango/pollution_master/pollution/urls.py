from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /pollution/custom
    path('custom/', views.custom, name='custom'),
    path('deleteCity/<int:id>', views.deleteCity, name='deleteCity'),
    path('custom/deleteStation/<int:id>',
         views.deleteStation, name='deleteStation'),
]
