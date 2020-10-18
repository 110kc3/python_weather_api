from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # ex: /weather/5/ -> /weather/Gliwice/
    path('<int:city_id>/', views.detail, name='detail'),
]