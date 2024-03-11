from django.contrib import admin
from .models import *

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','sub')
    list_display_links = ('first_name','last_name','email')
    list_filter = ('sub',)
    list_editable =('sub',)
admin.site.register(CustomUser,CustomUserAdmin)


class MissionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
admin.site.register(Mission,MissionAdmin)


class KindOfAnimalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
admin.site.register(KindOfAnimal,KindOfAnimalAdmin)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name','kind')
    list_display_links = ('name','kind')
admin.site.register(Breed,BreedAdmin)
class AnimalCardAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name','breed','birth','gender','color','search','mission')
    list_display_links = ('name',)
    list_filter = ('gender','search','mission')
    list_editable = ('search',)
admin.site.register(AnimalCard,AnimalCardAdmin)
class AdviceCardAdmin(admin.ModelAdmin):
    list_display = ('name','kind','breed','color','gender','lower_age','upper_age')
    list_display_links = ('name','kind')
    list_filter = ('kind','gender')
    list_editable = ('lower_age','upper_age')
admin.site.register(AdviceCard,AdviceCardAdmin)
class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'color')
    list_display_links = ('name',)

admin.site.register(Event,EventAdmin)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('event', 'date', 'pet','comment')
    list_display_links = ('date','comment')
    list_filter = ('pet', 'event')
admin.site.register(Calendar,CalendarAdmin)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('content', 'pet')
    list_display_links = ('content', )
    list_filter = ('pet',)
admin.site.register(Reviews,ReviewsAdmin)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('animal_who','animal_whom')
    list_display_links = ('animal_who',)
    list_filter = ('animal_who',)
admin.site.register(Like,LikeAdmin)
