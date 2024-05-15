from django.contrib.auth.forms import *
from .models import *


class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    connect = forms.CharField(label='Контактные данные', widget=forms.Textarea())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'email', 'connect', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    connect = forms.CharField(label='Контактные данные', widget=forms.Textarea())
    password = None
    confirm_password = None

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'connect')


class PasswordChangeForm(UserChangeForm):
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'autofocus': True}))
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'autofocus': True}))
    confirm_password = forms.CharField(label="Подтверждение нового пароля", strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}))
    first_name = None
    last_name = None
    email = None
    connect = None

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        user = self.instance
        if not user.check_password(old_password):
            raise forms.ValidationError("Вы ввели неверный старый пароль")
        return old_password

    def clean_new_password2(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('password',)


class AnimalAddForm(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=100)
    kind = forms.ModelChoiceField(queryset=KindOfAnimal.objects.all(), label='Вид животного', empty_label=' ', widget=forms.Select(attrs={'class':'left'}))
    breed = forms.ModelChoiceField(queryset=Breed.objects.none(), label='Порода', empty_label=None)
    birth = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), label='Пол', empty_label=' ', widget=forms.Select(attrs={'class':'left'}))
    color = forms.CharField(label='Окрас', max_length=100, widget=forms.TextInput(attrs={'class':'left'}))
    search = forms.BooleanField(label='Поиск', required=False)
    mission = forms.ModelChoiceField(queryset=Mission.objects.all(), label='Цель', required=False)
    photo = forms.ImageField(label='Фото', widget=forms.FileInput())
    comment = forms.CharField(label='Комментарий', max_length=100, widget=forms.Textarea())

    class Meta:
        model = AnimalCard
        fields = ['name', 'kind', 'breed', 'birth', 'gender', 'color', 'search', 'mission', 'photo', 'comment']

    def __init__(self, *args, **kwargs):
        super(AnimalAddForm, self).__init__(*args, **kwargs)

        if 'kind' in self.data:
            try:
                kind_id = int(self.data.get('kind'))
                self.fields['breed'].queryset = Breed.objects.filter(kind_id=kind_id).order_by('name')
            except (ValueError, TypeError):
                pass


class PetChangeForm(forms.ModelForm):
    search = forms.BooleanField(label='Поиск', required=False)
    mission = forms.ModelChoiceField(queryset=Mission.objects.all(), label='Цель', required=False)
    photo = forms.ImageField(label='Фото', widget=forms.FileInput())
    comment = forms.CharField(label='Комментарий', max_length=100, widget=forms.Textarea())

    class Meta:
        model = AnimalCard
        fields = ('search', 'mission', 'photo', 'comment')
