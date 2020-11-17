from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    # # ex: /pollution/custom
    # path('custom/', views.custom, name='custom'),
]
