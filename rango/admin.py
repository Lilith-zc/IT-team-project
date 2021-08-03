from django.contrib import admin
from rango.models import Category, Book, UserProfile, Author, Comment, LikeList

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'author')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'views')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'content', 'score')

class LikeListAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LikeList, LikeListAdmin)