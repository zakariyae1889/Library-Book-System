from django.contrib import admin
from .models import *
class GenreAdmin(admin.ModelAdmin):
    list_display=("name",'create','update')
    list_filter=("name",'create','update')
admin.site.register(Genre,GenreAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display=("Firstname","Lastname","Datebirth",'create','update')
    list_filter=("Firstname","Lastname","Datebirth",'create','update')
admin.site.register(Author,AuthorAdmin)

class PublisherAdmin(admin.ModelAdmin):
    list_display=("name","address","website",'create','update')
    list_filter=("name","address","website",'create','update')
admin.site.register(Publisher,PublisherAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre','publisher' ,'create','update')
    list_filter = ('title','author', 'publisher', 'genre','create','update')
admin.site.register(Book, BookAdmin)