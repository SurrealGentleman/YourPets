from django.contrib.auth import logout, update_session_auth_hash, login
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, FormView
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
                user = form_register.save()
                login(request, user)
                return redirect('profile')
                # form_register.save()
                # return redirect('main_page')
    return render(request, 'base.html', {'form_login': form_login, 'form_register': form_register})


def logout_user(request):
    logout(request)
    return redirect('main_page')




















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