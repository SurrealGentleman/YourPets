from django.contrib.auth.forms import *
from django.core.validators import RegexValidator
from django.forms import ModelForm, Form

from .models import *


class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    connect = forms.CharField(label='Контактные данные', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'email', 'connect', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    connect = forms.CharField(label='Контактные данные', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', required=False, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Подтверждение пароля', required=False, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'connect',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data


class SelectPets(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(SelectPets, self).__init__(*args, **kwargs)
        self.fields['pets'] = forms.ModelChoiceField(queryset=AnimalCard.objects.filter(owner=user),
                                                     widget=forms.Select(attrs={'class': 'select-with-button'}))
        self.fields['pets'].widget.choices = (list(self.fields['pets'].widget.choices) +
                                              [('add-pet_button', 'Добавить питомца')])


class AnimalAddForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    kind = forms.ModelChoiceField(queryset=KindOfAnimal.objects.all(), label='Вид животного', empty_label=' ')
    breed = forms.ModelChoiceField(queryset=Breed.objects.none(), label='Порода животного', empty_label=None)
    birth = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), label='Пол', empty_label=' ')
    color = forms.CharField(label='Окрас', max_length=100)
    search = forms.BooleanField(label='Поиск', required=False)
    mission = forms.ModelChoiceField(queryset=Mission.objects.all(), label='Цель', empty_label=' ')
    photo = forms.ImageField(label='Фото', widget=forms.FileInput())
    comment = forms.CharField(label='Комментарий', max_length=100)

    def __init__(self, *args, **kwargs):
        super(AnimalAddForm, self).__init__(*args, **kwargs)

        if 'kind' in self.data:
            try:
                kind_id = int(self.data.get('kind'))
                self.fields['breed'].queryset = Breed.objects.filter(kind_id=kind_id).order_by('name')
            except (ValueError, TypeError):
                pass
