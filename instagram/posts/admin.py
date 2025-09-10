from django.contrib import admin
from .models import Post ,CommentPost
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user','slug','created','edit_time','edited']
    list_filter = ("created","edited")

@admin.register(CommentPost)
class CommetPost(admin.ModelAdmin):
    list_display = ['user','post','created','edited','edited_date']
    list_filter = ('user','post')