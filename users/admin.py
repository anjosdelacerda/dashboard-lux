from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_filter = () 

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "email", "telefone")}),
        ("Informações da empresa", {"fields": ("empresa", "cargo", "identificador")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
        ("Chave única", {"fields": ("id",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "first_name", "password1", "password2",
                "email", "telefone", "empresa", "cargo", "identificador"
            ),
        }),
    )

    readonly_fields = ("last_login", "date_joined", "id")
    list_display = ("username", "email", "first_name", "empresa", "cargo", "identificador", "is_staff")
    search_fields = ("username", "email", "first_name", "cargo", "empresa__empresa", "identificador")
    ordering = ("username",)

    def has_delete_permission(self, request, obj=None):
        return False

    # Método para alterar o label do campo first_name
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['first_name'].label = 'Nome'
        return form

    # Opcional: Se quiser mudar também como aparece no list_display
    def first_name_display(self, obj):
        return obj.first_name
    first_name_display.short_description = 'Nome'

    # Substitui no list_display se quiser
    list_display = ("username", "email", "first_name_display", "empresa", "cargo", "identificador", "is_staff")

admin.site.register(User, CustomUserAdmin)