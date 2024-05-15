from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, FormView, DeleteView
from .forms import *


def login_or_register(request):
    form_login = CustomUserLoginForm()
    form_register = CustomUserCreationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            form_login = CustomUserLoginForm(request, data=request.POST)
            if form_login.is_valid():
                username = form_login.cleaned_data.get('username')
                password = form_login.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
        elif 'register' in request.POST:
            form_register = CustomUserCreationForm(request.POST)
            if form_register.is_valid():
                user = form_register.save(commit=False)
                user.set_password(form_register.cleaned_data['password1'])
                user.save()
                return redirect('main_page')
    return render(request, 'base.html', {'form_login': form_login, 'form_register': form_register})


def logout_user(request):
    logout(request)
    return redirect('main_page')


def profile(request):
    form_profile_change = CustomUserChangeForm(instance=request.user)
    form_password_change = PasswordChangeForm(instance=request.user)
    select_pets = AnimalCard.objects.filter(owner=request.user)
    if request.method == 'POST':
        if 'profile_change' in request.POST:
            form_profile_change = CustomUserChangeForm(request.POST, instance=request.user)
            if form_profile_change.is_valid():
                form_profile_change.save()
                messages.success(request, 'Профиль успешно изменен')
        elif 'password_change' in request.POST:
            form_password_change = PasswordChangeForm(request.POST, instance=request.user)
            if form_password_change.is_valid():
                form_password_change.save()
                messages.success(request, 'Пароль успешно изменен')
        elif 'pet_add' in request.POST:
            form_pet = AnimalAddForm(request.POST, request.FILES)
            if form_pet.is_valid():
                pet = form_pet.save(commit=False)
                pet.owner = request.user
                pet.save()
                messages.success(request, 'Питомец успешно создан')
        elif 'pet_change' in request.POST:
            pet = get_object_or_404(AnimalCard, pk=request.POST.get('pet'))
            form_pet = PetChangeForm(request.POST, request.FILES, instance=pet)
            if form_pet.is_valid():
                form_pet.save()
                messages.success(request, 'Данные о питомце успешно изменены')
        elif 'pet_delete' in request.POST:
            AnimalCard.objects.filter(pk=request.POST.get('pet')).delete()
            messages.success(request, 'Питомец успешно удален')

    context = {
        'form_profile_change': form_profile_change,
        'form_password_change': form_password_change,
        'select_pets': select_pets,
    }
    return render(request, 'profile.html', context)


def delete_user(request):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    user.delete()
    logout(request)
    return redirect('main_page')


def get_form_pet(request):
    context = dict()
    form = None
    if request.GET.get('add_pet'):
        form = AnimalAddForm()
        context['form_type'] = 'add'
    elif request.GET.get('update_pet'):
        data = AnimalCard.objects.get(id=request.GET.get('pet_id'))
        form = PetChangeForm(instance=data)
        context['form_type'] = 'update'
        context['pet_info'] = data
    context['form'] = form
    form_html = render_to_string('animal_add_form.html', context=context)
    return JsonResponse({'form_html': form_html})


def get_breeds(request):
    if request.GET.get('kind_id'):
        kind_id = request.GET.get('kind_id')  # Получаем идентификатор вида из запроса
        breeds = Breed.objects.filter(kind_id=kind_id).values('id', 'name')  # Получаем породы для выбранного вида
        return JsonResponse(list(breeds), safe=False)  # Отправляем данные в формате JSON
    elif request.GET.get('pet_id'):
        pet = AnimalCard.objects.get(pk=request.GET.get('pet_id'))
        breeds = Breed.objects.filter(kind_id=pet.kind).values('id', 'name')
        return JsonResponse(list(breeds), safe=False)


def pet_cards(request):
    # получаем всех питомцев авторизированного пользователя
    pet_user = AnimalCard.objects.filter(owner=request.user, search=True)

    # если нет питомцев, то рендерим страницу без формы
    if pet_user.count() == 0:
        return render(request, 'pet_cards.html')

    # форма фильтра
    form = Filter(user=request.user)

    # получаем данные из GET запроса
    pet_user_id = request.GET.get('pet')
    mission_id_list = request.GET.getlist('mission')
    gender_id_list = request.GET.getlist('gender')
    breed_id_list = request.GET.getlist('breed')

    # добавляем данные в форму для того, чтобы сохранялся выбор
    form.fields['pet'].initial = pet_user_id
    form.fields['mission'].initial = mission_id_list
    form.fields['gender'].initial = gender_id_list

    # получаем питомца по id из запроса
    if pet_user_id:
        pet = AnimalCard.objects.get(pk=pet_user_id)
    else:
        pet = None

# получаем список карточек животных по фильтру без тех кого уже лайкнули
    # все карточки животных других пользователей по фильтру
    animal_card_by_filter = AnimalCard.objects.filter(~Q(owner=request.user), mission__in=mission_id_list,
                                                      gender__in=gender_id_list, breed__in=breed_id_list)
    # все карточки животных которых лайкнул этот пет
    animal_cards_favorite = AnimalCard.objects.filter(animal_to_animal__animal_who=pet)
    # получаем их id
    animal_cards_favorite_ids = animal_cards_favorite.values_list('id', flat=True)
    # исключаем из списка карточек список лайкнутых карточек по id
    filtered_animal_card = animal_card_by_filter.exclude(id__in=animal_cards_favorite_ids)

    if request.method == 'POST':
        card = AnimalCard.objects.get(pk=request.POST.get('card_id'))
        Like.objects.create(animal_who=pet, animal_whom=card).save()

    return render(request, 'pet_cards.html', {'form': form, 'breed_list': breed_id_list,
                                              'cards': filtered_animal_card})


def likes(request):
    form = ChoicePet(user=request.user)
    return render(request, 'pet_likes.html', {'form': form})


def get_cards_likes(request):
    if request.GET.get('pet_id'):
        context = dict()
        # if request.GET.get('mutual_likes'):
        #     cards_likes_who = Like.objects.filter(animal_who=request.GET.get('pet_id'))
        #     cards_likes_whom = Like.objects.filter(animal_whom=request.GET.get('pet_id'))
        #     cards = AnimalCard.objects.filter(id__in=cards_likes.values_list('animal_who', flat=True))
        #     context['cards'] = cards
        # else:
        cards_likes = Like.objects.filter(animal_whom=request.GET.get('pet_id'))
        cards = AnimalCard.objects.filter(id__in=cards_likes.values_list('animal_who', flat=True))
        context['cards'] = cards
        cards_html = render_to_string('animal_card_likes.html', context=context)
        return JsonResponse({'cards_html': cards_html})
