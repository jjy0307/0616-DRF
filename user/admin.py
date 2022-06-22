from django.contrib import admin
from .models import CustomUser as CustomUserModel
from .models import UserProfile as UserProfileModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfileModel
    filter_horizontal = []

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'fullname', 'email')
    list_display_links = ('username', )
    list_filter = ('username', )
    search_fields = ('username', 'email', )

    fieldsets = (
        ("info", {'fields': ('username', 'password', 'email', 'fullname', 'join_date',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', )}),)

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date', )
        else:
            return ('join_date', )

    inlines = (
        UserProfileInline,
    )

admin.site.register(CustomUserModel, UserAdmin)