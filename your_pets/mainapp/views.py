from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
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
    form_pet = None
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


















def add_update_pet(request):
    context = dict()
    form = None
    if request.method == 'GET':
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

    elif request.method == 'POST':
        if 'pet_add' in request.POST:
            form_pet = AnimalAddForm(request.POST, request.FILES)
            if form_pet.is_valid():
                pet = form_pet.save(commit=False)
                pet.owner = request.user
                pet.save()
                messages.success(request, 'Питомец успешно создан')
                return redirect('profile')
        elif 'pet_change' in request.POST:
            pet = get_object_or_404(AnimalCard, pk=request.POST.get('pet'))
            form_pet = PetChangeForm(request.POST, request.FILES, instance=pet)
            if form_pet.is_valid():
                form_pet.save()
                messages.success(request, 'Данные о питомце успешно изменены')
        elif 'pet_delete' in request.POST:
            AnimalCard.objects.filter(pk=request.POST.get('pet')).delete()
            messages.success(request, 'Питомец успешно удален')





























# class ProfileUpdateView(UpdateView):
#     template_name = 'profile.html'
#     form_class = CustomUserChangeForm
#
#     def get_success_url(self):
#         return reverse_lazy('profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.save()
#         return super(ProfileUpdateView, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['select_pets'] = AnimalCard.objects.filter(owner=self.request.user)
#         return context


def delete_user(request):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    user.delete()
    logout(request)
    return redirect('main_page')


# class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
#     """
#     Изменение пароля пользователя
#     """
#     form_class = UserPasswordChangeForm
#     template_name = 'profile.html'
#     success_message = 'Ваш пароль был успешно изменён!'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Изменение пароля на сайте'
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('profile_detail', kwargs={'slug': self.request.user.profile.slug})

# def user_password_change(request):
#     print(request.method)
#     if request.method == 'GET':
#         form = UserPasswordChangeForm(request.user)
#         print(form)
#         form_html = render_to_string('password_change_form.html', {'form': form})
#         print(form_html)
#         return JsonResponse({'form_html': form_html})
#     elif request.method == 'POST':
#         pass











class AddPetView(CreateView):
    template_name = 'profile.html'
    form_class = AnimalAddForm

    def get_success_url(self):
        return reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        form_html = render_to_string('animal_add_form.html', {'form': self.get_form()})
        return JsonResponse({'form_html': form_html})


def pet_update(request):
    print(request.GET.get('pet_id'))
    data = AnimalCard.objects.get(id=request.GET.get('pet_id'))
    form = PetChangeForm(instance=data)
    print(form)
    form_html = render_to_string('animal_add_form.html', {'form': form})
    return JsonResponse({'form_html': form_html})

























# class ProfileUpdateView(UpdateView):
#     template_name = 'profile.html'
#     form_class = CustomUserChangeForm
#
#     def get_success_url(self):
#         return reverse_lazy('profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         password = form.cleaned_data.get("password")
#         if password:
#             user.set_password(password)
#             update_session_auth_hash(self.request, user)  # Сохранение пользователя в текущей сессии
#         user.save()
#         return super(ProfileUpdateView, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['select_pets'] = SelectPets(user=self.request.user)
#
#         # context['form_add_Pets'] = AnimalAddForm()
#         return context









# class MainPageView(ListView):
#     template_name = 'main_page.html'
#     context_object_name = 'forms'
#
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             context = {'form_login': CustomUserLoginForm(),
#                        'form_register': CustomUserCreationForm()}
#             return context
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

# class CustomFormView(ListView):
#     template_name = 'main_page.html'
#     form_class1 = CustomUserLoginForm
#     form_class2 = CustomUserCreationForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form1'] = self.form_class1()
#         context['form2'] = self.form_class2()
#         return context
#
#     def form_invalid(self, form1, form2):
#         return self.render_to_response(self.get_context_data(form1=form1, form2=form2))
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#
#     def post(self, request, *args, **kwargs):
#         form1 = self.form_class1(request.POST)
#         form2 = self.form_class2(request.POST)
#
#         if form1.is_valid():
#             username = form1.cleaned_data.get('username')
#             password = form1.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('profile'))
#         elif form2.is_valid():
#             form2.save()
#             return HttpResponseRedirect(reverse('profile'))
#         else:
#             return self.form_invalid(form1, form2)


# class SingInView(LoginView):
#     form_class = CustomUserLoginForm
#     template_name = 'main_page.html'
#
#     def form_invalid(self, form):
#         return render(self.request, self.template_name, {'form_login': form, 'form_er': form.errors})
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('profile')


# class SingUpView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'main_page.html'
#
#     def form_invalid(self, form):
#         return render(self.request, self.template_name, {'form_login': form, 'form_er': form.errors})
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('main_page')



















# class PetUpdateView(UpdateView):
#     template_name = 'profile.html'
#     form_class = PetChangeForm
#
#     def get_success_url(self):
#         return reverse_lazy('profile')
#
#     def get_object(self, queryset=None):
#         print(self.request.GET.get('pet_id'))
#         return AnimalCard.objects.get(pk=self.request.GET.get('pet_id'))
#
#     def form_valid(self, form):
#         form.save()
#         return super(PetUpdateView, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form_html'] = render_to_string('animal_add_form.html', {'form': self.get_form()})
#         return context




















# def add_card(request):
#     # if request.method == 'POST':
#     #     form = AnimalAddForm(request.POST)
#     #     if form.is_valid():
#     #         pass
#     # else:
#     #     form = AnimalAddForm()
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = SelectPets(request.POST)
#             if form.is_valid():
#                 pass
#         else:
#             form = SelectPets(user=request.user)
#     else:
#         form = 'ERROR'
#
#     return render(request, 'base.html', {'form': form})


def get_breeds(request):
    kind_id = request.GET.get('kind_id')  # Получаем идентификатор вида из запроса
    breeds = Breed.objects.filter(kind_id=kind_id).values('id', 'name')  # Получаем породы для выбранного вида
    return JsonResponse(list(breeds), safe=False)  # Отправляем данные в формате JSON

# def get_pet_info(request):
#     pet_id = request.GET.get('pet_id')
#     breeds = Breed.objects.filter(pet_id=pet_id).values('id', 'name')
#     return JsonResponse(list(breeds), safe=False)