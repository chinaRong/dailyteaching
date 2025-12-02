from django.urls import path
from .views import visitor_view
from .views import announcement


urlpatterns = [
    path('visitor/', visitor_view, name='visitor_view'),
    path('announcement/', announcement),
]

