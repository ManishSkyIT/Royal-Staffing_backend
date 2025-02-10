from django.contrib import admin
from .models import Role, RolePermission

class RolePermissionInline(admin.TabularInline):  
    model = RolePermission
    extra = 1

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [RolePermissionInline]  

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'permission_name', 'can_read', 'can_write')
