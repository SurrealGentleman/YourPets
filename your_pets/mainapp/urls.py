from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login_or_register, name='main_page'),
    path('logout/', logout_user, name='logout'),

    path('profile/', profile, name='profile'),

    path('delete/',  delete_user, name='delete_user'),

    path('get_form/', get_form_pet, name='get_form'),
    path('get_breeds/', get_breeds, name='get_breeds'),
    path('get_cards_likes/', get_cards_likes, name='get_cards_likes'),


    path('pet_cards/', pet_cards, name='pet_cards'),
    path('pet_cards/likes', likes, name='likes'),

    path('dislike/', dislike, name='dislike'),
    path('like/', like, name='like'),
    # path('add_update_pet/', add_update_pet, name='add_update_pet'),
    # path('change_password/', user_password_change, name='change_password'),
    # path('login/', login_or_register, name='login'),
    # path('registration/', SingUpView.as_view(), name='registration'),
    # path('change_pet/', add_update_pet, name='change_pet'),
    # path('', add_card, name='home'),
    # path('get_pet_info/', get_pet_info, name='get_pet_info'),
]

