from django.contrib import admin
from django.http import HttpRequest
from site_setup.models import MenuLink, SiteSetup
# Register your models here.

# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id', 'text', 'url_or_path',
#     list_display_links = 'id', 'text', 'url_or_path',
#     search_fields = 'id', 'text', 'url_or_path',
    
    
class MenuLinkInLine(admin.TabularInline):
    model = MenuLink
    extra = 1
    
    
@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',
    inlines = MenuLinkInLine,
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return not SiteSetup.objects.exists()