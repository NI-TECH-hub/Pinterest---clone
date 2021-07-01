from django.contrib import admin
from .models import AddPost,profile,comment
# Register your models here.

@admin.register(AddPost)
class postadmin(admin.ModelAdmin):
    list_display=['title','photo','published']

@admin.register(profile)
class adminuserdata(admin.ModelAdmin):
    list_display=['user']

@admin.register(comment)
class admincomment(admin.ModelAdmin):
    list_display =['user','post','content','time']

