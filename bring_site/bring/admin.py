from django.contrib import admin

from .models import *


@admin.register(Category)
class ModelCategory(admin.ModelAdmin):
    list_display = ['title', 'related_stuffs']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Stuff)
class ModelStuff(admin.ModelAdmin):
    list_display = ['title', 'rating', 'is_active', 'is_action', 'priority',
                    'price_per_ton', 'price_per_bag', 'price_per_piece', 'picture']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'email_verify', 'username']


@admin.register(Comment)
class ModelComment(admin.ModelAdmin):
    list_display = ['is_new', 'stuff', 'pub_comment_date', 'rating_vote', 'comment_text', 'author']
