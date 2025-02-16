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





#employees ka admin

from django.contrib import admin
from employees.models import EmployeesProfile

class EmployeesProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_address', 'authorised_person_name', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'company_name', 'authorised_person_name')

    actions = ['approve_employees', 'reject_employees']

    def approve_employees(self, request, queryset):
        queryset.update(status='approved')
    approve_employees.short_description = "Approve selected employees"

    def reject_employees(self, request, queryset):
        queryset.update(status='rejected')
    reject_employees.short_description = "Reject selected employees"

admin.site.register(EmployeesProfile, EmployeesProfileAdmin)
