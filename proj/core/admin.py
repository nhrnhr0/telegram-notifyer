from django.contrib import admin

from core.models import RegisteredUser,UnregisteredUser

# Register your models here.
class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegramId', 'lastMessageFromUserAt', 'LastNotifiedAt', 'preferedNotificationTime')
    list_filter = ('lastMessageFromUserAt', 'LastNotifiedAt')
    search_fields = ('name', 'telegramId')
    
    ordering = ('name',)
    readonly_fields = ('lastMessageFromUserAt', 'LastNotifiedAt')
    fieldsets = (
        (None, {
            'fields': ('name', 'telegramId')
        }),
        ('Notification', {
            'fields': ('lastMessageFromUserAt', 'LastNotifiedAt', 'preferedNotificationTime')
        }),
    )
    
    
    # def has_add_permission(self, request):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False
admin.site.register(RegisteredUser, RegisteredUserAdmin)


class UnregisteredUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'telegramId')
    list_filter = ('telegramId',)
    search_fields = ('username', 'telegramId')
    ordering = ('username',)
    readonly_fields = ('telegramId',)
    actions = ('register_user',)
    fieldsets = (
        (None, {
            'fields': ('username', 'telegramId')
        }),
    )
    def register_user(self, request, queryset):
        for user in queryset:
            user.register()
    # def has_add_permission(self, request):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False
admin.site.register(UnregisteredUser, UnregisteredUserAdmin)