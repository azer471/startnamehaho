from django.contrib import admin

# Register your models here.
from .models import Comment




class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author','object_id','content','timestamp','parent_id')

admin.site.register(Comment, CommentAdmin)
