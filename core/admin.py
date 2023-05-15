from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _

from goals.models import GoalCategory, Board
from .models import User


class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'username')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'avatar', 'timezone', 'bio', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    fieldsets_password = (
        (None, {'fields': ('password',)}),
    )

    # Добавляем возможность изменять пароль из Django admin
    def change_password(self, request, object_id, form_url='', extra_context=None):
        if '_changepassword' in request.POST:
            user = self.get_object(request, object_id)
            form = UserChangePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                msg = _('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
            messages.error(request, _('There was an error changing the password.'))
        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets = (
                (None, {'fields': ('username',)}),
                (None, {'fields': ('password',)}),
            ) + fieldsets[1:]
        return fieldsets

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_change_password'] = True
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(User, UserAdmin)


class UserChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format(**{'password_url': '../password/'})


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(GoalCategory, GoalCategoryAdmin)


class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated", "is_deleted")
    search_fields = ("title",)
    list_filter = ("is_deleted",)


admin.site.register(Board, BoardAdmin)
