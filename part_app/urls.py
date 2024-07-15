from django.urls import path
from .views import mark_view, model_view, search_part_view
urlpatterns = [
    path('mark/', mark_view, name='mark_view'),
    path('model/', model_view, name='model_view'),
    path('search/', search_part_view, name='search_view'),
]
