from datetime import date

from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, FormView, DeleteView
from .forms import *
from .parser import parse_exhibitions


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
                login(request, user)
                return redirect('profile')
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
                update_session_auth_hash(request, request.user)
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
    form = Filter(user=request.user)
    pet_user = AnimalCard.objects.filter(owner=request.user, search=True).first()
    breed_id_list = None
    cards = list()
    if request.method == 'POST':
        card = AnimalCard.objects.get(pk=request.POST.get('card_id'))
        if request.GET.get('pet'):
            pet_user = AnimalCard.objects.get(pk=request.GET.get('pet'))
        Like.objects.create(animal_who=pet_user, animal_whom=card).save()
    # if request.method == 'GET':  # открытие в первый раз или фильтр
    if not request.GET:  # открытие первый раз
        if pet_user is not None:
            cards_pets = AnimalCard.objects.filter(~Q(owner=request.user), search=True, kind=pet_user.kind)
            # все карточки животных которых лайкнул этот пет
            animal_cards_favorite = AnimalCard.objects.filter(animal_to_animal__animal_who=pet_user)
            # получаем их id
            animal_cards_favorite_ids = animal_cards_favorite.values_list('id', flat=True)
            # исключаем из списка карточек список лайкнутых карточек по id
            cards = cards_pets.exclude(id__in=animal_cards_favorite_ids)
            form.fields['pet'].initial = pet_user.pk
    else:  # фильтр
        pet_card = AnimalCard.objects.get(pk=request.GET.get('pet'))
        cards = AnimalCard.objects.filter(~Q(owner=request.user), search=True, kind=pet_card.kind)
        form.fields['pet'].initial = request.GET.get('pet')
        if request.GET.getlist('mission'):
            cards_mission = AnimalCard.objects.filter(~Q(owner=request.user), search=True, kind=pet_card.kind,
                                                      mission__in=request.GET.getlist('mission'))
            form.fields['mission'].initial = request.GET.getlist('mission')
        else:
            cards_mission = cards
        if request.GET.getlist('gender'):
            cards_gender = AnimalCard.objects.filter(~Q(owner=request.user), search=True, kind=pet_card.kind,
                                                     gender__in=request.GET.getlist('gender'))
            form.fields['gender'].initial = request.GET.getlist('gender')
        else:
            cards_gender = cards
        if request.GET.getlist('breed'):
            cards_breed = AnimalCard.objects.filter(~Q(owner=request.user), search=True, kind=pet_card.kind,
                                                    breed__in=request.GET.getlist('breed'))
            breed_id_list = request.GET.getlist('breed')
        else:
            cards_breed = cards

        filtered_animal_card = (cards_mission.filter(pk__in=cards_gender.values_list('pk', flat=True))
                                .filter(pk__in=cards_breed.values_list('pk', flat=True)))
        # все карточки животных которых лайкнул этот пет
        animal_cards_favorite = AnimalCard.objects.filter(animal_to_animal__animal_who=pet_card)
        # получаем их id
        animal_cards_favorite_ids = animal_cards_favorite.values_list('id', flat=True)
        # исключаем из списка карточек список лайкнутых карточек по id
        cards = filtered_animal_card.exclude(id__in=animal_cards_favorite_ids)
    return render(request, 'pet_cards.html', {'form': form, 'cards': cards, 'breed_list': breed_id_list})


def likes(request):
    form = ChoicePet(user=request.user)
    pet_user = AnimalCard.objects.filter(owner=request.user, search=True).first()
    if pet_user:
        form.fields['pet'].initial = pet_user.pk
    if request.method == 'POST':
        card = AnimalCard.objects.get(pk=request.POST.get('card_id'))
        if request.GET.get('pet'):
            pet_user = AnimalCard.objects.get(pk=request.GET.get('pet'))
        Like.objects.create(animal_who=pet_user, animal_whom=card).save()
    return render(request, 'pet_likes.html', {'form': form})


def get_cards_likes(request):
    if request.GET.get('pet_id'):

        cards_likes_whom = Like.objects.filter(animal_whom=request.GET.get('pet_id'))
        cards_whom = AnimalCard.objects.filter(id__in=cards_likes_whom.values_list('animal_who', flat=True))
        # кто лайкнул пета

        cards_likes_who = Like.objects.filter(animal_who=request.GET.get('pet_id'))
        cards_who = AnimalCard.objects.filter(id__in=cards_likes_who.values_list('animal_whom', flat=True))
        # кого лайкнул пета

        if request.GET.get('mutual_likes') == 'true':
            cards = cards_who.filter(id__in=cards_whom.values_list('id', flat=True))
        else:
            cards = cards_whom.exclude(id__in=cards_who)
        context = {'cards': cards, 'csrf_token': get_token(request), 'mutual': request.GET.get('mutual_likes')}
        cards_html = render_to_string('animal_card_likes.html', context=context)
        return JsonResponse({'cards_html': cards_html})


def dislike(request):
    if request.method == 'GET':
        who_pet = AnimalCard.objects.get(pk=request.GET.get('card_id'))
        whom_pet = AnimalCard.objects.get(pk=request.GET.get('petId'))
        Like.objects.get(animal_who=who_pet, animal_whom=whom_pet).delete()
        Like.objects.get(animal_who=whom_pet, animal_whom=who_pet).delete()
        return JsonResponse({'success': True})


def like(request):
    if request.method == 'GET':
        who_pet = AnimalCard.objects.get(pk=request.GET.get('petId'))
        whom_pet = AnimalCard.objects.get(pk=request.GET.get('card_id'))
        new_record = Like(animal_who=who_pet, animal_whom=whom_pet)
        new_record.save()
        return JsonResponse({'success': True})


def advice(request):
    form = ChoicePet(user=request.user)
    pet_user = AnimalCard.objects.filter(owner=request.user, search=True).first()
    if pet_user:
        form.fields['pet'].initial = pet_user.pk
    return render(request, 'advice.html', {'form': form})


def get_cards_advice(request):
    if request.GET.get('pet_id'):
        user_pet = AnimalCard.objects.get(id=request.GET.get('pet_id'))
        cards = AdviceCard.objects.filter(kind=user_pet.kind)
        favorites_cards = Favorites.objects.filter(pet=user_pet)
        context = {'cards': cards, 'favorites': favorites_cards}
        cards_html = render_to_string('advice_card.html', context=context)
        return JsonResponse({'cards_html': cards_html})


def favorites(request):
    form = ChoicePet(user=request.user)
    pet_user = AnimalCard.objects.filter(owner=request.user, search=True).first()
    if pet_user:
        form.fields['pet'].initial = pet_user.pk
    return render(request, 'favorites.html', {'form': form})


def get_cards_favorites_advice(request):
    if request.GET.get('pet_id'):
        user_pet = AnimalCard.objects.get(id=request.GET.get('pet_id'))
        favorites_cards_id = Favorites.objects.filter(pet=user_pet).values_list('advice', flat=True)
        cards = AdviceCard.objects.filter(pk__in=favorites_cards_id)
        favorites_cards = Favorites.objects.filter(pet=user_pet)
        context = {'cards': cards, 'favorites': favorites_cards}
        cards_html = render_to_string('advice_card.html', context=context)
        return JsonResponse({'cards_html': cards_html})


def favorite_advice_card(request):
    if request.GET.get('petId') and request.GET.get('advice_card_id'):
        user_pet = AnimalCard.objects.get(id=request.GET.get('petId'))
        advice_card = AdviceCard.objects.get(id=request.GET.get('advice_card_id'))
        new_record = Favorites(pet=user_pet, advice=advice_card)
        new_record.save()
        return JsonResponse({'success': True})


def not_favorite_advice_card(request):
    if request.GET.get('petId') and request.GET.get('advice_card_id'):
        user_pet = AnimalCard.objects.get(id=request.GET.get('petId'))
        advice_card = AdviceCard.objects.get(id=request.GET.get('advice_card_id'))
        Favorites.objects.get(pet=user_pet, advice=advice_card).delete()
        return JsonResponse({'success': True})


def exhibitions(request):
    list_events = parse_exhibitions()
    return render(request, 'exhibitions.html', {'list_events': list_events})


def calendar_current(request):
    if request.method == 'POST':
        form = CalendarForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    form = CalendarForm(user=request.user)
    calendar_events = Calendar.objects.filter(owner=request.user.pk, date__gte=date.today()).order_by('date')
    return render(request, 'calendar_current.html', {'form': form, 'calendar_events': calendar_events})


def calendar_last(request):
    calendar_events = Calendar.objects.filter(owner=request.user.pk, date__lt=date.today()).order_by('-date')
    return render(request, 'calendar_last.html', {'calendar_events': calendar_events})



















