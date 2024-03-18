from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=60, verbose_name='Имя')
    last_name = models.CharField(max_length=120, verbose_name='Фамилия')
    #geolocation =
    connect = models.CharField(max_length=160, verbose_name='Контактные данные')
    email = models.CharField(max_length=120, verbose_name='E-mail', unique=True)
    password = models.CharField(max_length=200, verbose_name='Пароль')
    sub = models.BooleanField(default=False, verbose_name='Подписка')
    username = None
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователь"
        ordering =['last_name','first_name']

class Mission(models.Model):
    name = models.CharField(max_length=60, verbose_name='Наименование цели', unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name="Цель"
        verbose_name_plural="Цели"

class KindOfAnimal(models.Model):
    name = models.CharField(max_length=60, verbose_name='Вид животного', unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name="Вид животного"
        verbose_name_plural="Виды животного"

class Breed(models.Model):
    name = models.CharField(max_length=60, verbose_name='Порода животного', unique=True)
    kind = models.ForeignKey(KindOfAnimal,on_delete=models.CASCADE, verbose_name='Вид животного')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name="Порода животного"
        verbose_name_plural="Породы животного"

class Gender(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name="Пол"
        verbose_name_plural="Пол"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

class AnimalCard(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Хозяин')
    name = models.CharField(max_length=60, verbose_name='Кличка')
    kind = models.ForeignKey(KindOfAnimal,on_delete=models.CASCADE, verbose_name='Вид животного')
    breed = models.ForeignKey(Breed,on_delete=models.CASCADE, verbose_name='Порода')
    birth = models.DateField(verbose_name='Дата рождения')
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE, verbose_name='Пол')
    color = models.CharField(max_length=60, verbose_name='Окрас')
    search = models.BooleanField(default=False, verbose_name='Поиск')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, verbose_name='Цель')
    # geolocation =
    photo = models.ImageField(upload_to="images/pets/",verbose_name='Фото')
    comment = models.CharField(max_length=100, null = False, blank = False,verbose_name='Комментарий')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name="Карточка животного"
        verbose_name_plural="Карточки животного"
        ordering = ['name']

class Like(models.Model):
    animal_who = models.ForeignKey(AnimalCard,on_delete=models.CASCADE, verbose_name="Кто лайкнул")
    animal_whom = models.ForeignKey(AnimalCard,related_name='animal_to_animal',on_delete=models.CASCADE, verbose_name='Кого лайкнули')

    class Meta:
        verbose_name="Лайк"
        verbose_name_plural="Лайки"

class Reviews(models.Model):
    content = models.CharField(max_length=100, verbose_name='Отзыв')
    pet = models.ForeignKey(AnimalCard, on_delete=models.CASCADE, verbose_name='Питомец')

    def __str__(self):
        return f"{self.content}"

    class Meta:
        verbose_name="Отзыв"
        verbose_name_plural="Отзывы"

class Event(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Наименование события',unique=True)
    color = models.CharField(verbose_name='Цвет', unique=True,max_length=30)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name="Событие"
        verbose_name_plural="Событие"

class Calendar(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, verbose_name='Событие')
    date = models.DateTimeField(verbose_name='Дата')
    pet = models.ForeignKey(AnimalCard,on_delete=models.CASCADE, verbose_name='Питомец')
    comment = models.CharField(max_length=100, verbose_name='Комментарий',null=True, blank=True)

    def __str__(self):
        return f"{self.event}"

    class Meta:
        verbose_name="Календарь"
        verbose_name_plural="Календарь"

class AdviceCard(models.Model):
    name = models.CharField(max_length=100, verbose_name='Заголовок')
    kind = models.ForeignKey(KindOfAnimal,on_delete=models.CASCADE, verbose_name='Вид животного')
    breed = models.ForeignKey(Breed,on_delete=models.CASCADE, verbose_name='Порода',null=True,blank=True)
    color = models.CharField(max_length=60, verbose_name='Окрас',null=True,blank=True)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE, verbose_name='Пол',null=True,blank=True)
    lower_age = models.IntegerField(verbose_name='Нижний диапазон',null=True,blank=True)
    upper_age = models.IntegerField(verbose_name='Верхний диапазон',null=True,blank=True)
    content = models.CharField(max_length=230, verbose_name='Содержание')

    def __str__(self):
        return f"{self.content}"

    class Meta:
        verbose_name="Карточка советов"
        verbose_name_plural="Карточка советов"
        ordering=['kind','content']

class Favorites(models.Model):
    pet = models.ForeignKey(AnimalCard,on_delete=models.CASCADE, verbose_name='Питомец')
    advice = models.ForeignKey(AdviceCard,on_delete=models.CASCADE, verbose_name='Совет')

    class Meta:
        verbose_name="Избранный совет"
        verbose_name_plural="Избранные советы"
        ordering = ['pet']

