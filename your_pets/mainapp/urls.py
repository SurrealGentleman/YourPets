from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', login_or_register, name='main_page'),
    path('logout/', logout_user, name='logout'),

    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    # path('login/', login_or_register, name='login'),
    # path('registration/', SingUpView.as_view(), name='registration'),


    path('add_pet/', AddPetView.as_view(), name='add_pet'),
    path('change_pet/', pet_update, name='change_pet'),

    path('get_breeds/', get_breeds, name='get_breeds'),

    # path('', add_card, name='home'),
    path('get_pet_info/', get_pet_info, name='get_pet_info'),
]
