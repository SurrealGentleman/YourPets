from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from .forms import *


class MainPageView(ListView):
    template_name = 'main_page.html'
    context_object_name = 'forms'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            context = {'form_login': CustomUserLoginForm(),
                       'form_register': CustomUserCreationForm()}
            return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SingInView(LoginView):
    form_class = CustomUserLoginForm
    template_name = 'main_page.html'

    def get_success_url(self):
        return reverse_lazy('profile')


class SingUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main_page.html'

    def get_success_url(self):
        return reverse_lazy('main_page')


def logout_user(request):
    logout(request)
    return redirect('main_page')


class ProfileUpdateView(UpdateView):
    template_name = 'profile.html'
    form_class = CustomUserChangeForm

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        if password:
            user.set_password(password)
            update_session_auth_hash(self.request, user)  # Сохранение пользователя в текущей сессии
        user.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_pets'] = SelectPets(user=self.request.user)

        # context['form_add_Pets'] = AnimalAddForm()
        return context


class AddPetView(CreateView):
    form_class = AnimalAddForm
    template_name = 'profile.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        form_html = render_to_string('animal_add_form.html', {'form': self.get_form()})
        return JsonResponse({'form_html': form_html})






def add_card(request):
    # if request.method == 'POST':
    #     form = AnimalAddForm(request.POST)
    #     if form.is_valid():
    #         pass
    # else:
    #     form = AnimalAddForm()
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SelectPets(request.POST)
            if form.is_valid():
                pass
        else:
            form = SelectPets(user=request.user)
    else:
        form = 'ERROR'

    return render(request, 'base.html', {'form': form})


def get_breeds(request):
    kind_id = request.GET.get('kind_id')  # Получаем идентификатор вида из запроса
    breeds = Breed.objects.filter(kind_id=kind_id).values('id', 'name')  # Получаем породы для выбранного вида
    return JsonResponse(list(breeds), safe=False)  # Отправляем данные в формате JSON

def get_pet_info(request):
    pet_id = request.GET.get('pet_id')
    breeds = Breed.objects.filter(pet_id=pet_id).values('id', 'name')
    return JsonResponse(list(breeds), safe=False)
