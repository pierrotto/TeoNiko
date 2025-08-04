from django.contrib import admin

from TeoNiko.jewels.choices import GemShapeChoices
from TeoNiko.jewels.models import Jewel, Metal, Gem, Material, Category, Photo


@admin.register(Jewel)
class JewelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weight')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    verbose_name_plural = 'Categories'
    search_fields = ('name',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'description', 'jewel', 'category')
    search_fields = ('name',)


@admin.register(Metal)
class MetalAdmin(admin.ModelAdmin):
    list_display = ('type', 'weight')
    search_fields = ('type',)


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    list_display = ('type', 'weight')
    search_fields = ('type',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('type', 'weight')
    search_fields = ('type',)
