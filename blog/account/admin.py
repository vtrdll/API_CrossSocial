from django.contrib import admin
from .models import Profile, Box, Times, Time_Achievements
# Register your models here.



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_coach', 'box', 'category')
    list_filter = ('is_coach', 'box', 'category')
    search_fields = ('user__username',)
    

admin.site.register(Profile, ProfileAdmin)



class BoxAdmin(admin.ModelAdmin):
    list_display = ('box_name')
    list_filter = ('box_name')
    search_fields = ('box_name', 'author')

admin.site.register(Box)


class TimeAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'box', 'category', 'placement', 'achievements')
    list_filter = ('name',)
    search_fields = ('name' , 'creator')


admin.site.register(Times)


class Time_AchievementsAdmin(admin.ModelAdmin):
    list_display = ('time', 'achievement', 'placement')
    list_filter = ('time',)
    search_fields = ('time__name' , 'achievement')

admin.site.register(Time_Achievements)