from django.contrib import admin
from .models import Empresa
from users.models import User

class FuncionariosInline(admin.TabularInline):
    model = User
    fields = ("username","first_name","email", "cargo", "identificador")
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "gestor_responsavel_fk":
            kwargs["queryset"] = User.objects.filter(is_gestor=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Empresa, EmpresaAdmin)
