from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.RestaurantViewSet.as_view({'get': 'list'}), name='all_restaurant'),
    path('create/', views.RestaurantCreateView.as_view(), name='create_restaurant'),
    path('menu/upload/', views.MenuCreateView.as_view(), name='upload_menu'),
    path('menu/today/', views.TodayMenuView.as_view(), name='today_menu'),
]
