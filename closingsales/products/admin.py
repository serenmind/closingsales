from django.contrib import admin

# Register your models here.
from .models import Category, Subcategory, Advertisement, AdImage

class CategoryAdmin(admin.ModelAdmin):
	exclude = ('slug', 'image')


class SubcategoryAdmin(admin.ModelAdmin):
	exclude = ('slug', 'image')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register([Advertisement, AdImage])
