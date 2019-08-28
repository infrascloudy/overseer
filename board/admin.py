from django.contrib import admin
from .models import Category, Service, Status, Event


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class StatusAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "severity")
    prepopulated_fields = {"slug": ("name",)}


class EventAdmin(admin.ModelAdmin):
    list_display = ("start", "service", "status", "message")
    list_filter = ("service", "status")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Event, EventAdmin)
