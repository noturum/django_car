from django.urls import path, include

from . import views
from .views import (
    APICommentListCreateView,
    APICarsListCreateView,
    APICarRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/new/', views.CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_edit'),
    path('car/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
    path('api/cars/<int:id>/comments/', APICommentListCreateView.as_view(), name='api_car_comments'),
    path('api/cars/<int:id>/', APICarRetrieveUpdateDestroyView.as_view(), name='api_car_edit'),
    path('api/cars/', APICarsListCreateView.as_view(), name='api_car_list'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
