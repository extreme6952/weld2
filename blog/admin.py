from django.contrib import admin

from .models import Movie,Comment


@admin.register(Movie)

class MovieAdmin(admin.ModelAdmin):

    list_display = ['title','slug','publish','status']

    list_filter = ['status','created','publish']

    search_fields = ['title','description']

    prepopulated_fields = {'slug':('title',)}

    date_hierarchy = 'publish'

    ordering = ['status','publish']



@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):

    list_display = ['name','email','movie','created','active']

    list_filter = ['active','created','updated']

    search_fields = ['body','email','name']



