from django.contrib import admin
from .models import *

# Register your models here.
class MyBlogAdmin(admin.ModelAdmin):
     list_display = ['category', 'title', 'created_date']

admin.site.register(Category)
admin.site.register(Blog, MyBlogAdmin)
admin.site.register(PostData)