from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('login/', SingInView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', SingUpView.as_view(), name='registration'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    path('add_pet/', AddPetView.as_view(), name='add_pet'),
    path('get_breeds/', get_breeds, name='get_breeds'),

    # path('', add_card, name='home'),
    path('get_pet_info/', get_pet_info, name='get_pet_info'),
]