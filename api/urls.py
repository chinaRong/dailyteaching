from django.urls import path
from .views import visitor_view

urlpatterns = [
    path('visitor/', visitor_view, name='visitor_view'),
]

