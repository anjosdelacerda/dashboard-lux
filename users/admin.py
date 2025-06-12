# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User, Gestor
from django.utils.html import format_html 
from django.urls import reverse 
from django.utils.safestring import mark_safe


class CustomUserAdmin(UserAdmin):
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
    list_display = ("username", "email", "first_name_display", "empresa", "cargo", "identificador", "is_staff")
    search_fields = ("username", "email", "first_name", "cargo", "empresa__empresa", "identificador")
    ordering = ("username",)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['first_name'].label = 'Nome'
        return form

    def first_name_display(self, obj):
        return obj.first_name
    first_name_display.short_description = 'Nome'

admin.site.register(User, CustomUserAdmin)

class GestorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name_display', 'telefone', 'view_funcionarios_link')
    list_filter = ()
    search_fields = ('username', 'email', 'first_name')
    readonly_fields = ('id', 'last_login', 'date_joined', 'funcionarios_list')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "email", "telefone")}),
        ("Funcionários gerenciados", {"fields": ("funcionarios_list",)}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_gestor=True)

    def first_name_display(self, obj):
        return obj.first_name
    first_name_display.short_description = 'Nome'

    def funcionarios_list(self, obj):
        funcionarios = obj.get_funcionarios()
        if not funcionarios.exists():
            return "Nenhum funcionário gerenciado"
        
        html = "<ul>"
        for func in funcionarios:
            html += f"<li>{func.first_name} ({func.email}), {func.telefone} - {func.empresa.empresa if func.empresa else 'Sem empresa'} - {func.cargo}</li>"
        html += "</ul>"
        return mark_safe(html)
    funcionarios_list.short_description = "Funcionários Gerenciados"

    def view_funcionarios_link(self, obj):
        count = obj.get_funcionarios().count()
        url = reverse('admin:users_user_changelist') + f'?empresa__gestor_responsavel_fk__id__exact={obj.id}'
        return format_html('<a href="{}">{} Funcionário(s)</a>', url, count)
    view_funcionarios_link.short_description = "Funcionários"

admin.site.register(Gestor, GestorAdmin)