from django.contrib import admin
from rango.models import Category, Page, UserProfile


# This PageAdmin class inherits from admin.ModelAdmin
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


# This class customises the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
