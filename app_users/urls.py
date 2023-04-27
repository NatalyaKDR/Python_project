from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('main/', main, name='main'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', MyRegisterView, name='register'),
    path('/', MyLogoutView.as_view(), name='logout'),
    path('items/<int:pk>', item_details, name="item-details"),
    path('add/', add, name='add'),
    path('update/<str:pk>/',update, name='update'),
    path('delete/<str:pk>/',delete, name='delete'),
    path('my_tests/<test>', get_test, name='test'),
]
