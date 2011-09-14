from django.contrib import admin
from pcstore.store.models import *

class AuthorAdmin(admin.ModelAdmin): pass

admin.site.register(Category, AuthorAdmin)
admin.site.register(Producer, AuthorAdmin)
admin.site.register(Product, AuthorAdmin)
admin.site.register(Order, AuthorAdmin)

