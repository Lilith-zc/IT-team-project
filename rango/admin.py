from django.contrib import admin
from rango.models import Category, Page, UserProfile

class Pagelist(admin.ModelAdmin):
    list_display = ('title', 'category', 'url','views')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','views','likes')
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, Pagelist)
admin.site.register(UserProfile)
