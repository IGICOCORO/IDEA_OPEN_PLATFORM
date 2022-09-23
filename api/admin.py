from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
	list_display = "name", "content","created_by","is_liked"
	search_fields = "name", "content","is_liked" 
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = "post","name","comment","created_on"
	search_fields = "name","created_on","comment"