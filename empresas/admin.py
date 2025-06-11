from django.contrib import admin
from .models import Empresa
from users.models import User

class FuncionariosInline(admin.TabularInline):
    model = User
    fields = ("username", "email", "cargo", "identificador")
    extra = 0
    readonly_fields = fields
    can_delete = False
    show_change_link = True

class EmpresaAdmin(admin.ModelAdmin):
    list_filter = () 
    list_display = ("empresa", "cnpj", "distribuidora", "modalidade_tarifaria", "gestor_nome")
    search_fields = ("empresa", "cnpj", "distribuidora")
    readonly_fields = ("id",)
    inlines = [FuncionariosInline]

    def gestor_nome(self, obj):
        return obj.gestor_responsavel_fk.get_full_name() if obj.gestor_responsavel_fk else "—"
    gestor_nome.short_description = "Gestor Responsável"

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Empresa, EmpresaAdmin)
